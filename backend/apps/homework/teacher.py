import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.courses.models import Course

from .models import Homework


@method_decorator(csrf_exempt, name="dispatch")
class TeacherHomeworkListView(View):
    """Homework the logged-in teacher has assigned — list + create."""

    def get(self, request):
        homework = Homework.objects.filter(course__teacher=request.user).values(
            "id", "course_id", "title", "description", "due_date", "created_at"
        )
        return JsonResponse({"results": list(homework)})

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"detail": "Invalid JSON body"}, status=400)

        course = Course.objects.filter(id=payload.get("course_id"), teacher=request.user).first()
        if course is None:
            return JsonResponse(
                {"detail": "course_id is required and must be one of your classes"}, status=400
            )

        homework = Homework(
            course=course,
            title=payload.get("title", ""),
            description=payload.get("description", ""),
            due_date=payload.get("due_date") or None,
            created_by=request.user,
        )
        try:
            homework.full_clean()
        except ValidationError as exc:
            return JsonResponse({"detail": exc.message_dict}, status=400)
        homework.save()

        return JsonResponse(
            {"id": homework.id, "course_id": course.id, "title": homework.title}, status=201
        )
