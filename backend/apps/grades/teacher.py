import json

from django.http import JsonResponse
from django.views import View

from apps.courses.models import Course

from .models import Grade


class TeacherGradeListCreateView(View):
    """Teacher enters/edits grades for courses they own — never someone else's."""

    def get(self, request):
        grades = Grade.objects.filter(course__teacher=request.user).values(
            "id", "course_id", "student_id", "value", "created_at"
        )
        return JsonResponse({"results": list(grades)})

    def post(self, request):
        payload = json.loads(request.body)
        course = Course.objects.filter(id=payload.get("course_id"), teacher=request.user).first()
        if course is None:
            return JsonResponse({"detail": "Course not found or not yours"}, status=404)

        grade = Grade.objects.create(
            course=course,
            student_id=payload.get("student_id"),
            entered_by=request.user,
            value=payload.get("value"),
        )
        return JsonResponse({"id": grade.id}, status=201)
