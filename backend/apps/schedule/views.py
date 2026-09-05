from django.http import JsonResponse
from django.views import View

from .models import Lesson


class LessonListView(View):
    def get(self, request):
        lessons = Lesson.objects.values("id", "course_id", "starts_at", "ends_at", "room")
        return JsonResponse({"results": list(lessons)})
