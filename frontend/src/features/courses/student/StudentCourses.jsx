import { useTranslation } from 'react-i18next'

export default function StudentCourses() {
  const { t } = useTranslation()
  return <h2>{t('nav.courses')}</h2>
}
