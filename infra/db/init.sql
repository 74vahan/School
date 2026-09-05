-- Runs once, on first container start, before the app's migrations.
-- Table schema itself belongs to the backend's migrations (Django/FastAPI),
-- not here — this file only bootstraps what migrations can't create themselves.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Enforces the three fixed roles at the DB level too, not just in app code,
-- per school-project-conventions (teacher/student/guest, no synonyms).
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM ('teacher', 'student', 'guest');
    END IF;
END
$$;
