from django.conf import settings
from django.db import models

from apps.courses.models import Course


class Homework(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="homework")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="homework_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.course.title_ru})"
