from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.roles import GUEST, ROLE_CHOICES
from apps.common.validators import validate_technical_identifier


class User(AbstractUser):
    # Replaces AbstractUser's default Unicode-permissive username validator —
    # login is a technical field, Latin-only per school-project-conventions.
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        validators=[validate_technical_identifier],
        error_messages={"unique": "A user with that username already exists."},
    )
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default=GUEST)
