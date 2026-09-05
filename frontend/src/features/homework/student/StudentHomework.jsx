import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { api } from '../../../shared/api/client'

// The student's main screen after login — "может видеть домашнюю работу".
export default function StudentHomework() {
  const { t } = useTranslation()
  const [homework, setHomework] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/student/homework/')
      .then((data) => setHomework(data.results))
      .catch(() => setError(t('common.error.loadFailed')))
  }, [t])

  return (
    <div className="page-wide">
      <h2>{t('nav.homework')}</h2>
      {error && <p role="alert">{error}</p>}
      {homework.length === 0 && !error && <p className="empty">{t('homework.empty')}</p>}
      <ul>
        {homework.map((hw) => (
          <li key={hw.id} className="section">
            <strong>{hw.title}</strong>
            {hw.due_date && (
              <p className="empty">
                {t('homework.dueDate')}: {hw.due_date}
              </p>
            )}
            {hw.description && <p>{hw.description}</p>}
          </li>
        ))}
      </ul>
    </div>
  )
}
