import { createContext, useContext, useEffect, useState } from 'react'
import { auth } from './auth'

const AuthContext = createContext(null)

// The backend authenticates via session cookie; /api/me/ is the source of
// truth. On mount we ask it who's logged in instead of trusting anything
// client-side, so a stale or tampered client guess can never grant access —
// `loading` covers that round trip so ProtectedRoute doesn't flash the
// wrong screen while it's in flight.
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    auth
      .me()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  async function register(username, password) {
    const data = await auth.register(username, password)
    setUser(data)
    return data
  }

  async function login(username, password) {
    const data = await auth.login(username, password)
    setUser(data)
    return data
  }

  async function logout() {
    await auth.logout().catch(() => {})
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
