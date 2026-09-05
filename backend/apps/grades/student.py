from django.http import JsonResponse
from django.views import View

from .models import Grade


class StudentGradeListView(View):
    """Student reads own grades only — never another student's, never write access."""

    def get(self, request):
        grades = Grade.objects.filter(student=request.user).values(
            "id", "course_id", "value", "created_at"
        )
        return JsonResponse({"results": list(grades)})
