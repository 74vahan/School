// Same allowlist rule as infra/db/init.sql's `login` CHECK constraint —
// technical fields (login, slugs, filenames) must stay Latin-only, even
// though the rest of the UI is ru/en/hy. Keep this in sync with the backend
// regex per school-project-conventions.
const LATIN_ONLY = /^[a-zA-Z0-9_.-]+$/

export function isLatinOnly(value) {
  return LATIN_ONLY.test(value)
}
