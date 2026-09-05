from django.urls import path

from .guest import LoginView, RegisterView
from .student import StudentProfileView
from .teacher import AssignGuestView, PendingGuestsView, TeacherProfileView

teacher_patterns = [
    path("profile/", TeacherProfileView.as_view(), name="teacher-profile"),
    path("pending-guests/", PendingGuestsView.as_view(), name="teacher-pending-guests"),
    path(
        "pending-guests/<int:user_id>/assign/",
        AssignGuestView.as_view(),
        name="teacher-assign-guest",
    ),
]
student_patterns = [path("profile/", StudentProfileView.as_view(), name="student-profile")]
guest_patterns = [
    path("login/", LoginView.as_view(), name="guest-login"),
    path("register/", RegisterView.as_view(), name="guest-register"),
]
