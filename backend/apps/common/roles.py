TEACHER = "teacher"
STUDENT = "student"
GUEST = "guest"

# Exact lowercase strings only, in code, DB enums, and JWT/session claims —
# per school-project-conventions. Matches infra/db/init.sql's user_role enum.
ROLE_CHOICES = [
    (TEACHER, "Teacher"),
    (STUDENT, "Student"),
    (GUEST, "Guest"),
]
