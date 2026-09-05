from django.urls import path

from .student import StudentCourseListView
from .teacher import TeacherCourseListView, TeacherCourseStudentsView

teacher_patterns = [
    path("", TeacherCourseListView.as_view(), name="teacher-courses"),
    path(
        "<int:course_id>/students/",
        TeacherCourseStudentsView.as_view(),
        name="teacher-course-students",
    ),
]
student_patterns = [path("", StudentCourseListView.as_view(), name="student-courses")]
