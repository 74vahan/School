from django.http import JsonResponse
from django.views import View

from .models import Course


class StudentCourseListView(View):
    """Courses the logged-in student is enrolled in — read-only."""

    def get(self, request):
        courses = Course.objects.filter(students=request.user).values(
            "id", "title_ru", "title_en", "title_hy", "slug"
        )
        return JsonResponse({"results": list(courses)})
