// Where each role lands right after login/register. A guest has no class
// yet, so it goes to the pending page (styled like a 404), not a real page —
// per school-project-conventions ("guest может только входить/регистрироваться").
export function roleHome(role) {
  switch (role) {
    case 'teacher':
      return '/teacher/admin'
    case 'student':
      return '/student/homework'
    default:
      return '/pending'
  }
}
