from django.urls import path

from .student import StudentHomeworkListView
from .teacher import TeacherHomeworkListView

teacher_patterns = [path("", TeacherHomeworkListView.as_view(), name="teacher-homework")]
student_patterns = [path("", StudentHomeworkListView.as_view(), name="student-homework")]
