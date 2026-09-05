import { useTranslation } from 'react-i18next'

export default function TeacherCourses() {
  const { t } = useTranslation()
  return <h2>{t('nav.courses')}</h2>
}
