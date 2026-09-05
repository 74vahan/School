import { useTranslation } from 'react-i18next'

export default function StudentGrades() {
  const { t } = useTranslation()
  return <h2>{t('nav.grades')}</h2>
}
