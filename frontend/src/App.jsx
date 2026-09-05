import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { AuthProvider } from './shared/api/AuthContext'
import ProtectedRoute from './shared/ui/ProtectedRoute'

import Login from './features/users/Login'
import Register from './features/users/Register'
import PendingPage from './features/users/PendingPage'
import StudentHomework from './features/homework/student/StudentHomework'
import TeacherAdmin from './features/admin/TeacherAdmin'

// Guest can only log in or register; a logged-in guest with no class yet
// lands on /pending; student's main screen is homework; teacher's is the
// admin page — per school-project-conventions.
export default function App() {
  const { t } = useTranslation()

  return (
    <AuthProvider>
      <BrowserRouter>
        <header className="app-header">
          <h1>{t('app.title')}</h1>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/pending" element={<PendingPage />} />
            <Route
              path="/student/homework"
              element={
                <ProtectedRoute role="student">
                  <StudentHomework />
                </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/admin"
              element={
                <ProtectedRoute role="teacher">
                  <TeacherAdmin />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<PendingPage />} />
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  )
}
