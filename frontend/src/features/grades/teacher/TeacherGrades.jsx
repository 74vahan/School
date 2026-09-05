import { useTranslation } from 'react-i18next'

// Teacher view: enter/edit grades. Kept separate from the student view
// (read-only, own grades only) even though both live in features/grades.
export default function TeacherGrades() {
  const { t } = useTranslation()
  return <h2>{t('nav.grades')}</h2>
}
