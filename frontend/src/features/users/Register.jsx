import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { isLatinOnly } from '../../shared/ui/validators'
import { useAuth } from '../../shared/api/AuthContext'

// Every new account starts as `guest` — becoming a student happens only
// when a teacher assigns it to a class (features/homework/teacher/TeacherAdmin.jsx).
export default function Register() {
  const { t } = useTranslation()
  const { register } = useAuth()
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
    if (username && !isLatinOnly(username)) return

    try {
      await register(username, password)
      navigate('/pending')
    } catch {
      setError(t('auth.error.registerFailed'))
    }
  }

  return (
    <div className="page">
      <form onSubmit={handleSubmit}>
        <h2>{t('auth.register')}</h2>
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
        <button type="submit">{t('auth.register')}</button>
        <p>
          <Link to="/login">{t('auth.login')}</Link>
        </p>
      </form>
    </div>
  )
}
