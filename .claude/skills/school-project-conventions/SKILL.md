---
name: school-project-conventions
description: Project conventions for the school website (teacher/student/guest roles, Django/FastAPI + PostgreSQL backend, Docker + nginx, Terraform on GCP, GitHub Actions CI/CD). Use this whenever creating or editing files under ci-cd/ or infra/, writing Terraform, Dockerfiles, nginx configs, GitHub Actions workflows, or backend code that deals with roles/permissions/auth in this repo — even if the user doesn't mention "conventions" explicitly.
---

# School Project Conventions

This repo builds a school website with three roles — **teacher**, **student**, **guest** — plus the infrastructure to run it. Follow these conventions so the two halves of the project (application code and infrastructure) stay consistent and don't drift apart as different people/sessions touch them.

## Repository layout

Three top-level folders, each with a single responsibility:

```
frontend/                   # React (Vite) SPA — talks to the backend only via /api
├── src/
│   ├── features/           # domain-grouped, see "Frontend structure" below
│   ├── shared/              # api client, cross-feature UI, validators
│   └── locales/{ru,en,hy}/ # i18n resource files
├── Dockerfile               # multi-stage: node build -> non-root nginx serving dist/
└── nginx.static.conf         # internal-only static server, port 8080

ci-cd/                      # everything about building & shipping the app images
├── .github/workflows/      # GitHub Actions pipelines (lint, test, build, deploy)
└── docker/
    └── Dockerfile          # backend application image (multi-stage build)

infra/                      # everything about the running environment
├── terraform/              # GCP infrastructure as code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── backend.tf          # remote state config
├── docker-compose.yml       # app + nginx + db, wired together for the VM
├── nginx/
│   └── nginx.conf
└── db/
    └── init.sql             # schema bootstrap / seed data
```

Keep this split strict: application build/deploy logic lives in `ci-cd/`, anything about the server and its running containers lives in `infra/`. If you're unsure where a new file goes, ask "does this describe how we build the app, or how/where it runs?"

## Backend structure: grouped by domain, not a monolith

Don't build one flat Django app (or one FastAPI router file) holding all the logic. Split the backend into domain modules — e.g. `users`, `courses`, `grades`, `schedule` — each an independent Django app (or FastAPI router package). This is what keeps the codebase navigable as it grows: a change to grading logic should only ever touch the `grades` module.

Within each domain module, further split by role where the role's logic actually differs (not just a permission check, but genuinely different behavior/serializers/templates):

```
apps/
├── users/
│   ├── teacher.py      # teacher-facing views/serializers
│   ├── student.py      # student-facing views/serializers
│   ├── guest.py
│   └── models.py       # shared models for this domain
├── courses/
│   ├── teacher.py
│   ├── student.py
│   └── models.py
├── grades/
│   ├── teacher.py       # enter/edit grades
│   ├── student.py       # read own grades only
│   └── models.py
└── schedule/
    └── ...
```

A domain module with only one relevant role (e.g. `schedule` might be read-only for everyone) doesn't need the role split — don't force the pattern where it adds no value. The rule is: **domain is the primary split, role is the secondary split inside it** — never the other way around (don't create a top-level `teacher/` folder containing bits of every domain).

## Frontend structure (frontend/, React + Vite)

The frontend is a separate SPA, not templates baked into the backend — it only ever talks to the backend through `/api/*` (see `infra/nginx/nginx.conf`, which routes `/api/` to the backend and everything else to the frontend container). Mirror the backend's domain-first, role-second split under `src/features/`:

```
src/features/
├── courses/{teacher,student}/
├── grades/{teacher,student}/
├── schedule/                # no role split — same read-only view for everyone
└── users/                   # login/auth, shared across roles
```

Same rule as the backend: split by domain first, by role only where the role's view genuinely differs, and don't force a role split where one view serves everyone (e.g. `schedule/`).

`src/shared/` holds things that cut across features: the API client (`shared/api/client.js`), reusable UI, and validators. Don't duplicate the API base URL or fetch boilerplate inside individual feature files — go through `shared/api`.

## Internationalization (i18n)

The site ships in **three languages: Russian (`ru`), English (`en`), Armenian (`hy`)**. Design the i18n layer to make adding a fourth language later a translation-file change, not a code change:

- All user-facing strings go through the framework's translation layer: `gettext`/`{% trans %}` on the backend (Django, or an equivalent for FastAPI + templates), `react-i18next` with `src/locales/{ru,en,hy}/common.json` on the frontend — never hardcode UI text in a single language in views/templates/components.
- Locale is content, not logic: role-based behavior (teacher/student/guest) must never be branched on language. Keep the two orthogonal.
- Store per-language content (course names, announcements, etc.) either as translation files (`locale/ru/`, `locale/en/`, `locale/hy/`) for static UI strings, or as language-suffixed DB columns/tables for user-generated content that needs translation — decide per-field, but be consistent within a domain module.
- Default language and fallback order should be explicit in settings (e.g. `ru` default, falling back to `en` if a translation is missing) rather than left to framework defaults.

## Cyrillic validation

Because the site is multilingual, **Cyrillic input is expected in user-facing content** (names, course titles, announcements) — that's normal and must not be blocked. The restriction is narrower: **technical fields must be Latin-only**, enforced both client-side and server-side (not just a linter/CI check) so users get immediate feedback on the site itself:

- Blocked from Cyrillic (and any non-ASCII): login/username, URL slugs, filenames for uploads, DB/API keys and identifiers, environment variable names.
- Validate with an explicit allowlist regex (e.g. `^[a-zA-Z0-9_.-]+$`) on these fields, not a Cyrillic-specific blocklist — an allowlist also catches Armenian script and other non-Latin input in the same fields without needing a second rule.
- Show a clear inline validation error in the relevant language when a technical field is rejected, rather than a generic 400 — this is a real user-facing check, not just server-side hardening.

## Roles & naming conventions

Three roles only: `teacher`, `student`, `guest` — always these exact lowercase strings in code, DB enums, and JWT/session claims. Don't introduce synonyms (`admin`, `pupil`, `visitor`) for the same concepts.

- **guest** is unauthenticated or minimally-authenticated read access — never gets write endpoints.
- **student** can read their own data and submit work; never gets access to other students' data or grading endpoints.
- **teacher** can manage classes, grades, and content for the classes they own — not a superuser role. If you need a true superuser, call it `admin` explicitly and treat it as a fourth, separate role rather than overloading `teacher`.

API endpoints are grouped by role prefix so permission boundaries are visible at a glance:
```
/api/teacher/...
/api/student/...
/api/guest/...        (or unprefixed public routes, if truly public)
```
Enforce the role check at the routing/middleware layer, not just in the view logic — a route under `/api/teacher/` should 403 for anyone without that role before the handler runs.

## Terraform (infra/terraform, GCP)

- **Remote state, never local.** Configure a GCS backend in `backend.tf` — local state in a repo with multiple contributors (or CI) leads to lock conflicts and drift. Never commit `.tfstate` files.
- **All environment-specific values go through `variables.tf`**, with a `terraform.tfvars` that's git-ignored (commit a `terraform.tfvars.example` instead). Nothing environment-specific (project ID, region, machine type) hardcoded in `main.tf`.
- **Secrets never enter `.tf` files or state in plaintext** where avoidable — pull DB passwords and API keys from Google Secret Manager or inject them via CI secrets, not `variable` defaults.
- Pin the `google` provider version in `main.tf` (`required_providers` block) so `terraform apply` doesn't silently pick up breaking provider changes.
- Tag/label every resource with the project name and environment (e.g. `labels = { project = "school-site", env = "prod" }`) — this is what makes cost and blast-radius visible later when the infra grows past one VM.

## Docker & nginx (ci-cd/docker, infra)

- **Multi-stage Dockerfile**: a build stage with full toolchain, a slim final stage (e.g. `python:3.x-slim`) with only runtime deps. Keeps the shipped image small and reduces attack surface.
- **Run as a non-root user** in the final stage (`USER app`, with the user created explicitly) — never run the app process as root in the container.
- **nginx is the only edge-facing service.** The app container should not be directly reachable from outside the docker network; nginx proxies to it. Enable:
  - Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `Referrer-Policy`).
  - TLS termination at nginx (don't terminate TLS in the app).
  - Client body size limits appropriate for the school site's use (assignment file uploads etc.) — don't leave nginx defaults if uploads are a feature.
- Database credentials and any secrets reach containers via environment variables sourced from a `.env` file (git-ignored) or GitHub Secrets in CI — never hardcoded in `docker-compose.yml` or the Dockerfile.

## CI/CD (ci-cd/.github/workflows, GitHub Actions)

- **Pin every third-party action to a full commit SHA**, not a floating tag (`uses: actions/checkout@<sha> # v4.x.x`) — floating tags are a supply-chain risk since the action's maintainer can push new code under the same tag.
- **Scope `GITHUB_TOKEN` permissions explicitly** per workflow (`permissions: contents: read` etc.) rather than relying on the repo-wide default, and grant write scopes only to the job that actually needs them (e.g. only the deploy job gets `id-token: write` for GCP auth).
- **All secrets (GCP service account key or Workload Identity config, DB passwords, registry credentials) live in GitHub Secrets**, referenced as `${{ secrets.NAME }}` — never inline, never in a committed `.env` checked into `ci-cd/`.
- Prefer **Workload Identity Federation** over a long-lived GCP service account JSON key for deploy jobs, since Terraform is targeting GCP — ask before introducing a static key if WIF isn't already set up, since that's a meaningful security tradeoff.
- Typical pipeline shape: `lint/test` → `build image` → `push to registry` → `terraform plan` (on PR) / `terraform apply` (on merge to main) → `deploy`. Keep `terraform apply` gated to the main branch only; PRs should only ever `plan`.
