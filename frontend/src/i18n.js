import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

import ru from './locales/ru/common.json'
import en from './locales/en/common.json'
import hy from './locales/hy/common.json'

// Site ships in ru/en/hy (school-project-conventions). Language is content,
// never branched on for role-based (teacher/student/guest) behavior.
i18n.use(initReactI18next).init({
  resources: {
    ru: { common: ru },
    en: { common: en },
    hy: { common: hy },
  },
  lng: 'ru',
  fallbackLng: 'en',
  ns: ['common'],
  defaultNS: 'common',
  interpolation: { escapeValue: false },
})

export default i18n
