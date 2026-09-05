from django.http import JsonResponse

# Enforced at the middleware layer so a request under the wrong role prefix
# 403s before the view handler runs, per school-project-conventions.
# /api/guest/ is intentionally not listed here — guest is public access.
ROLE_PREFIXES = {
    "/api/teacher/": "teacher",
    "/api/student/": "student",
}


class RolePrefixAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for prefix, required_role in ROLE_PREFIXES.items():
            if request.path.startswith(prefix):
                if getattr(request.user, "role", None) != required_role:
                    return JsonResponse({"detail": "Forbidden"}, status=403)
                break
        return self.get_response(request)
