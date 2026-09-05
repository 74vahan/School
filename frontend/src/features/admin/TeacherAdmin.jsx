import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { api } from '../../shared/api/client'
import { isLatinOnly } from '../../shared/ui/validators'

// The teacher's admin page — cuts across users (pending guests), courses
// (classes/rosters) and homework, so it gets its own top-level feature
// rather than living inside one domain module.
export default function TeacherAdmin() {
  const { t } = useTranslation()
  const [guests, setGuests] = useState([])
  const [classes, setClasses] = useState([])
  const [selectedClassId, setSelectedClassId] = useState(null)
  const [roster, setRoster] = useState(null)
  const [error, setError] = useState('')

  function refreshGuests() {
    api.get('/teacher/users/pending-guests/').then((data) => setGuests(data.results))
  }

  function refreshClasses() {
    api.get('/teacher/courses/').then((data) => setClasses(data.results))
  }

  useEffect(() => {
    refreshGuests()
    refreshClasses()
  }, [])

  async function handleAssign(guestId, courseId) {
    if (!courseId) return
    try {
      await api.post(`/teacher/users/pending-guests/${guestId}/assign/`, { course_id: Number(courseId) })
      refreshGuests()
      if (Number(courseId) === selectedClassId) loadRoster(selectedClassId)
    } catch {
      setError(t('admin.error.assignFailed'))
    }
  }

  async function handleCreateClass(e) {
    e.preventDefault()
    const form = e.target
    const slug = form.slug.value
    if (!isLatinOnly(slug)) {
      setError(t('auth.login.error.latinOnly'))
      return
    }
    try {
      await api.post('/teacher/courses/', {
        title_ru: form.title_ru.value,
        title_en: form.title_en.value,
        title_hy: form.title_hy.value,
        slug,
      })
      form.reset()
      refreshClasses()
    } catch {
      setError(t('admin.error.classCreateFailed'))
    }
  }

  function loadRoster(courseId) {
    setSelectedClassId(courseId)
    api.get(`/teacher/courses/${courseId}/students/`).then(setRoster)
  }

  async function handleCreateHomework(e) {
    e.preventDefault()
    const form = e.target
    try {
      await api.post('/teacher/homework/', {
        course_id: Number(form.course_id.value),
        title: form.title.value,
        description: form.description.value,
        due_date: form.due_date.value || null,
      })
      form.reset()
    } catch {
      setError(t('admin.error.homeworkCreateFailed'))
    }
  }

  return (
    <div className="page-wide">
      <h2>{t('admin.title')}</h2>
      {error && <p role="alert">{error}</p>}

      <section className="section">
        <h3>{t('admin.pendingGuests')}</h3>
        {guests.length === 0 && <p className="empty">{t('admin.noPendingGuests')}</p>}
        <ul>
          {guests.map((guest) => (
            <li key={guest.id} className="list-row">
              {guest.username}
              <select defaultValue="" onChange={(e) => handleAssign(guest.id, e.target.value)}>
                <option value="" disabled>
                  {t('admin.assignToClass')}
                </option>
                {classes.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.title_ru}
                  </option>
                ))}
              </select>
            </li>
          ))}
        </ul>
      </section>

      <section className="section">
        <h3>{t('admin.createClass')}</h3>
        <form onSubmit={handleCreateClass}>
          <input name="title_ru" placeholder={t('admin.classTitleRu')} required />
          <input name="title_en" placeholder={t('admin.classTitleEn')} required />
          <input name="title_hy" placeholder={t('admin.classTitleHy')} required />
          <input name="slug" placeholder="slug (latin)" required />
          <button type="submit">{t('admin.createClass')}</button>
        </form>
      </section>

      <section className="section">
        <h3>{t('admin.classRoster')}</h3>
        <ul>
          {classes.map((c) => (
            <li key={c.id} className="list-row">
              <button type="button" onClick={() => loadRoster(c.id)}>
                {c.title_ru}
              </button>
            </li>
          ))}
        </ul>
        {roster && (
          <ul>
            {roster.students.map((s) => (
              <li key={s.id} className="list-row">
                {s.username}
              </li>
            ))}
            {roster.students.length === 0 && <li className="empty">{t('admin.noStudents')}</li>}
          </ul>
        )}
      </section>

      <section className="section">
        <h3>{t('admin.createHomework')}</h3>
        <form onSubmit={handleCreateHomework}>
          <select name="course_id" required defaultValue="">
            <option value="" disabled>
              {t('admin.selectClass')}
            </option>
            {classes.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title_ru}
              </option>
            ))}
          </select>
          <input name="title" placeholder={t('admin.homeworkTitle')} required />
          <textarea name="description" placeholder={t('admin.homeworkDescription')} />
          <input name="due_date" type="date" />
          <button type="submit">{t('admin.createHomework')}</button>
        </form>
      </section>
    </div>
  )
}
