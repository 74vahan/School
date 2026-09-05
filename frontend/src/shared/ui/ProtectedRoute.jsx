import { Navigate } from 'react-router-dom'
import { useAuth } from '../api/AuthContext'

// Guards a route by role. A guest (or anyone whose role doesn't match)
// bounces to the pending/"404" page rather than seeing the real content —
// this is a client-side courtesy redirect only; the backend's
// RolePrefixAccessMiddleware is what actually enforces access.
export default function ProtectedRoute({ role, children }) {
  const { user } = useAuth()

  if (!user) return <Navigate to="/login" replace />
  if (user.role !== role) return <Navigate to="/pending" replace />

  return children
}
