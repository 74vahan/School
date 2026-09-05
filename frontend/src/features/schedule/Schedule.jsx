import { useTranslation } from 'react-i18next'

// Read-only for every role — no teacher/student split needed here,
// per school-project-conventions ("don't force the pattern where it adds no value").
export default function Schedule() {
  const { t } = useTranslation()
  return <h2>{t('nav.schedule')}</h2>
}
