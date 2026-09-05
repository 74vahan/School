from django.db import models

from apps.courses.models import Course


class Lesson(models.Model):
    # Read-only for every role — no teacher/student split needed here,
    # per school-project-conventions ("don't force the pattern where it adds no value").
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    room = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["starts_at"]
