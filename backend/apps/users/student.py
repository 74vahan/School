from django.http import JsonResponse
from django.views import View


class StudentProfileView(View):
    """Student-facing profile — placeholder until real profile fields exist."""

    def get(self, request):
        return JsonResponse({"username": request.user.username, "role": request.user.role})
