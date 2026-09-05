from django.contrib import admin
from django.urls import include, path

from apps.courses.urls import student_patterns as courses_student
from apps.courses.urls import teacher_patterns as courses_teacher
from apps.grades.urls import student_patterns as grades_student
from apps.grades.urls import teacher_patterns as grades_teacher
from apps.homework.urls import student_patterns as homework_student
from apps.homework.urls import teacher_patterns as homework_teacher
from apps.schedule.urls import urlpatterns as schedule_patterns
from apps.users.urls import guest_patterns as users_guest
from apps.users.urls import student_patterns as users_student
from apps.users.urls import teacher_patterns as users_teacher

# Grouped by role prefix so permission boundaries are visible at a glance,
# per school-project-conventions. The actual enforcement happens in
# apps.common.middleware.RolePrefixAccessMiddleware, not here.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/teacher/users/", include(users_teacher)),
    path("api/student/users/", include(users_student)),
    path("api/guest/users/", include(users_guest)),
    path("api/teacher/courses/", include(courses_teacher)),
    path("api/student/courses/", include(courses_student)),
    path("api/teacher/grades/", include(grades_teacher)),
    path("api/student/grades/", include(grades_student)),
    path("api/teacher/homework/", include(homework_teacher)),
    path("api/student/homework/", include(homework_student)),
    path("api/schedule/", include(schedule_patterns)),
]
