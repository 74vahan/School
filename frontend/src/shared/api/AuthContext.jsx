import { createContext, useContext, useState } from 'react'
import { auth } from './auth'

const AuthContext = createContext(null)

const STORAGE_KEY = 'school-site.user'

// The backend authenticates via session cookie, not a token — there's no
// `/api/*/me` endpoint yet, so we just remember what login/register last
// told us (username, role) to survive a page refresh. The cookie is what
// actually gates access; this is only a client-side echo of it.
function readStoredUser() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(readStoredUser)

  function persist(data) {
    setUser(data)
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  }

  async function register(username, password) {
    const data = await auth.register(username, password)
    persist(data)
    return data
  }

  async function login(username, password) {
    const data = await auth.login(username, password)
    persist(data)
    return data
  }

  function logout() {
    setUser(null)
    sessionStorage.removeItem(STORAGE_KEY)
  }

  return (
    <AuthContext.Provider value={{ user, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
