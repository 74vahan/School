from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class MeView(View):
    """Role-agnostic 'who am I' — outside the /api/{teacher,student}/ prefixes
    on purpose, so RolePrefixAccessMiddleware never blocks it. Lets the
    frontend verify the session-echoed role in sessionStorage against the
    server on load, instead of trusting it blindly until the next API call."""

    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Not authenticated"}, status=401)
        return JsonResponse({"username": request.user.username, "role": request.user.role})


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"detail": "Logged out"})
