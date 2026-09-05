from django.conf import settings
from django.db import models

from apps.common.validators import validate_technical_identifier


class Course(models.Model):
    # User-generated content (course names) is per-language DB columns, not
    # translation files — those are for static UI strings only, per
    # school-project-conventions i18n rules.
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_hy = models.CharField(max_length=200)

    # Technical identifier used in URLs — Latin-only, same rule as login.
    slug = models.SlugField(max_length=100, unique=True, validators=[validate_technical_identifier])

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="courses_taught"
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="courses_enrolled", blank=True
    )

    def __str__(self):
        return self.title_ru
