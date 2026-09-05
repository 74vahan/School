from django.http import JsonResponse
from django.views import View

from .models import Homework


class StudentHomeworkListView(View):
    """Homework for classes the logged-in student is enrolled in — read-only.

    This is the main student-facing screen (memory.md: "после входа может
    видеть домашнюю работу").
    """

    def get(self, request):
        homework = Homework.objects.filter(course__students=request.user).values(
            "id", "course_id", "title", "description", "due_date", "created_at"
        )
        return JsonResponse({"results": list(homework)})
