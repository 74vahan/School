import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from apps.common.roles import GUEST, STUDENT, TEACHER
from apps.courses.models import Course

User = get_user_model()

pytestmark = pytest.mark.django_db


def register(client, username, password="pass12345"):
    return client.post(
        "/api/guest/users/register/",
        data={"username": username, "password": password},
        content_type="application/json",
    )


def create_course(teacher_client, slug):
    resp = teacher_client.post(
        "/api/teacher/courses/",
        data={"title_ru": "Матем", "title_en": "Math", "title_hy": "Մաթ", "slug": slug},
        content_type="application/json",
    )
    assert resp.status_code == 201, resp.content
    return resp.json()["id"]


def test_register_creates_guest_role():
    client = Client()
    resp = register(client, "newguest")

    assert resp.status_code == 201
    assert resp.json()["role"] == GUEST
    assert User.objects.get(username="newguest").role == GUEST


def test_register_rejects_duplicate_username():
    client = Client()
    register(client, "dupe")
    resp = register(Client(), "dupe")

    assert resp.status_code == 409


def test_guest_is_403d_out_of_teacher_and_student_routes():
    client = Client()
    register(client, "guest1")

    assert client.get("/api/teacher/courses/").status_code == 403
    assert client.get("/api/student/homework/").status_code == 403


def test_teacher_assigning_guest_promotes_to_student():
    teacher = User.objects.create_user(username="teacher1", password="x", role=TEACHER)
    teacher_client = Client()
    teacher_client.force_login(teacher)

    guest_client = Client()
    register(guest_client, "guest2")
    guest = User.objects.get(username="guest2")

    course_id = create_course(teacher_client, "math-1")

    pending = teacher_client.get("/api/teacher/users/pending-guests/")
    assert any(g["username"] == "guest2" for g in pending.json()["results"])

    assign_resp = teacher_client.post(
        f"/api/teacher/users/pending-guests/{guest.id}/assign/",
        data={"course_id": course_id},
        content_type="application/json",
    )

    assert assign_resp.status_code == 200
    guest.refresh_from_db()
    assert guest.role == STUDENT
    assert Course.objects.get(id=course_id).students.filter(id=guest.id).exists()


def test_assigning_already_assigned_guest_is_rejected():
    teacher = User.objects.create_user(username="teacher2", password="x", role=TEACHER)
    teacher_client = Client()
    teacher_client.force_login(teacher)

    guest_client = Client()
    register(guest_client, "guest3")
    guest = User.objects.get(username="guest3")
    course_id = create_course(teacher_client, "math-2")

    first = teacher_client.post(
        f"/api/teacher/users/pending-guests/{guest.id}/assign/",
        data={"course_id": course_id},
        content_type="application/json",
    )
    assert first.status_code == 200

    second = teacher_client.post(
        f"/api/teacher/users/pending-guests/{guest.id}/assign/",
        data={"course_id": course_id},
        content_type="application/json",
    )
    assert second.status_code == 404


def test_student_sees_own_homework_but_not_teacher_routes():
    teacher = User.objects.create_user(username="teacher3", password="x", role=TEACHER)
    student = User.objects.create_user(username="student1", password="x", role=STUDENT)

    teacher_client = Client()
    teacher_client.force_login(teacher)
    course_id = create_course(teacher_client, "physics-1")
    Course.objects.get(id=course_id).students.add(student)

    hw_resp = teacher_client.post(
        "/api/teacher/homework/",
        data={"course_id": course_id, "title": "Read ch.1"},
        content_type="application/json",
    )
    assert hw_resp.status_code == 201

    student_client = Client()
    student_client.force_login(student)

    assert student_client.get("/api/teacher/homework/").status_code == 403

    hw_list = student_client.get("/api/student/homework/")
    assert hw_list.status_code == 200
    assert len(hw_list.json()["results"]) == 1


def test_student_does_not_see_other_classes_homework():
    teacher = User.objects.create_user(username="teacher4", password="x", role=TEACHER)
    outsider = User.objects.create_user(username="student2", password="x", role=STUDENT)

    teacher_client = Client()
    teacher_client.force_login(teacher)
    course_id = create_course(teacher_client, "chemistry-1")
    teacher_client.post(
        "/api/teacher/homework/",
        data={"course_id": course_id, "title": "Read ch.2"},
        content_type="application/json",
    )

    outsider_client = Client()
    outsider_client.force_login(outsider)
    hw_list = outsider_client.get("/api/student/homework/")

    assert hw_list.json()["results"] == []


def test_me_endpoint_reflects_session_and_requires_auth():
    client = Client()
    assert client.get("/api/me/").status_code == 401

    register(client, "guest4")
    me = client.get("/api/me/")
    assert me.status_code == 200
    assert me.json() == {"username": "guest4", "role": GUEST}


def test_logout_clears_session():
    client = Client()
    register(client, "guest5")
    assert client.get("/api/me/").status_code == 200

    logout_resp = client.post("/api/logout/", data={}, content_type="application/json")
    assert logout_resp.status_code == 200
    assert client.get("/api/me/").status_code == 401
