from django.urls import path

from .student import StudentGradeListView
from .teacher import TeacherGradeListCreateView

teacher_patterns = [path("", TeacherGradeListCreateView.as_view(), name="teacher-grades")]
student_patterns = [path("", StudentGradeListView.as_view(), name="student-grades")]
