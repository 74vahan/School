import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Course


@method_decorator(csrf_exempt, name="dispatch")
class TeacherCourseListView(View):
    """Classes the logged-in teacher owns — list + create.

    `Course` doubles as "class" here (a teacher, a roster of students) —
    there's no separate class concept, per the guest->student assignment
    flow in apps.users.teacher.AssignGuestView.
    """

    def get(self, request):
        courses = Course.objects.filter(teacher=request.user).values(
            "id", "title_ru", "title_en", "title_hy", "slug"
        )
        return JsonResponse({"results": list(courses)})

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"detail": "Invalid JSON body"}, status=400)

        course = Course(
            title_ru=payload.get("title_ru", ""),
            title_en=payload.get("title_en", ""),
            title_hy=payload.get("title_hy", ""),
            slug=payload.get("slug", ""),
            teacher=request.user,
        )
        try:
            course.full_clean(exclude=["students"])
        except ValidationError as exc:
            return JsonResponse({"detail": exc.message_dict}, status=400)
        course.save()

        return JsonResponse(
            {"id": course.id, "title_ru": course.title_ru, "slug": course.slug}, status=201
        )


class TeacherCourseStudentsView(View):
    """Roster of one class — "список учеников по классам"."""

    def get(self, request, course_id):
        course = Course.objects.filter(id=course_id, teacher=request.user).first()
        if course is None:
            return JsonResponse({"detail": "Not found"}, status=404)

        students = list(course.students.values("id", "username"))
        return JsonResponse({"id": course.id, "title_ru": course.title_ru, "students": students})
