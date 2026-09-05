import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.common.roles import GUEST, STUDENT
from apps.courses.models import Course

from .models import User


class TeacherProfileView(View):
    """Teacher-facing profile — placeholder until real profile fields exist."""

    def get(self, request):
        return JsonResponse({"username": request.user.username, "role": request.user.role})


class PendingGuestsView(View):
    """Guests who registered but haven't been assigned to a class yet —
    shown on the teacher's admin page (memory.md: "видеть кто только
    зарегнулся")."""

    def get(self, request):
        guests = User.objects.filter(role=GUEST).order_by("date_joined").values(
            "id", "username", "date_joined"
        )
        return JsonResponse({"results": list(guests)})


@method_decorator(csrf_exempt, name="dispatch")
class AssignGuestView(View):
    """Promotes a guest to student by enrolling them in a class (Course).

    This is the one place `role` moves from GUEST to STUDENT — a guest can
    never self-promote, only a teacher assigning them to a class does it.
    """

    def post(self, request, user_id):
        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"detail": "Invalid JSON body"}, status=400)

        course = Course.objects.filter(id=payload.get("course_id"), teacher=request.user).first()
        if course is None:
            return JsonResponse(
                {"detail": "course_id is required and must be one of your classes"}, status=400
            )

        guest = User.objects.filter(id=user_id, role=GUEST).first()
        if guest is None:
            return JsonResponse({"detail": "Guest not found or already assigned"}, status=404)

        guest.role = STUDENT
        guest.save(update_fields=["role"])
        course.students.add(guest)

        return JsonResponse({"id": guest.id, "username": guest.username, "role": guest.role})
