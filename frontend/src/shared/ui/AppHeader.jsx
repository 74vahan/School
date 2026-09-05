import { useTranslation } from 'react-i18next'
import { useAuth } from '../api/AuthContext'

export default function AppHeader() {
  const { t } = useTranslation()
  const { user, logout } = useAuth()

  return (
    <header className="app-header">
      <h1>{t('app.title')}</h1>
      {user && (
        <nav className="app-nav">
          <span>{user.username}</span>
          <button type="button" onClick={logout}>
            {t('auth.logout')}
          </button>
        </nav>
      )}
    </header>
  )
}
