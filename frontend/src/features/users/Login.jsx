import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { isLatinOnly } from '../../shared/ui/validators'
import { useAuth } from '../../shared/api/AuthContext'
import { roleHome } from './roleHome'

// Guest's entry point — matches school-project-conventions: a guest can
// only log in or register, nothing else.
export default function Login() {
  const { t } = useTranslation()
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  function handleUsernameChange(e) {
    const value = e.target.value
    setUsername(value)
    setError(value && !isLatinOnly(value) ? t('auth.login.error.latinOnly') : '')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      const { role } = await login(username, password)
      navigate(roleHome(role))
    } catch {
      setError(t('auth.error.invalidCredentials'))
    }
  }

  return (
    <div className="page">
      <form onSubmit={handleSubmit}>
        <h2>{t('auth.login')}</h2>
        <div>
          <label htmlFor="username">{t('auth.login')}</label>
          <input id="username" value={username} onChange={handleUsernameChange} />
        </div>

        <div>
          <label htmlFor="password">{t('auth.password')}</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {error && <p role="alert">{error}</p>}
        <button type="submit">{t('auth.login')}</button>
        <p>
          <Link to="/register">{t('auth.register')}</Link>
        </p>
      </form>
    </div>
  )
}
