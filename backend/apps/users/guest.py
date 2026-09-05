import json

from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.common.roles import GUEST

User = get_user_model()


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    """Public entry point — matches frontend/src/features/users/Login.jsx.

    Login itself is validated Latin-only both here (via User.username's
    validator, enforced on the auth backend's lookup) and client-side.
    """

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"detail": "Invalid JSON body"}, status=400)

        username = payload.get("username", "")
        password = payload.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({"detail": "Invalid credentials"}, status=401)

        login(request, user)
        return JsonResponse({"username": user.username, "role": user.role})


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    """Guest self-registration.

    A new account always starts as `role=GUEST` with no class — only a
    teacher can promote it to `student` by assigning it to a class
    (see apps.users.teacher.AssignGuestView). Until that happens, the
    frontend routes a guest to a friendly "nothing here yet" page for any
    page beyond login/register, per school-project-conventions.
    """

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"detail": "Invalid JSON body"}, status=400)

        username = payload.get("username", "")
        password = payload.get("password", "")

        if not username or not password:
            return JsonResponse({"detail": "username and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"detail": "Username already taken"}, status=409)

        user = User(username=username, role=GUEST)
        user.set_password(password)
        try:
            user.full_clean()
        except ValidationError as exc:
            return JsonResponse({"detail": exc.message_dict}, status=400)
        user.save()

        login(request, user)
        return JsonResponse({"username": user.username, "role": user.role}, status=201)
