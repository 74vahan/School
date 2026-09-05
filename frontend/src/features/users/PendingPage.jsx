import { useTranslation } from 'react-i18next'

// Shown to a guest for any page beyond login/register — they registered,
// but a teacher hasn't assigned them to a class yet, so there's genuinely
// nothing to show. Styled like a friendly 404 rather than a real error,
// per school-project-conventions ("после рега выдаёт красивую 404 страницу").
export default function PendingPage() {
  const { t } = useTranslation()

  return (
    <div className="page-center">
      <h1>404</h1>
      <p>{t('pending.message')}</p>
    </div>
  )
}
