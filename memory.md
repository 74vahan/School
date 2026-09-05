# Project Progress / TODO

Живой трекер состояния проекта. Обновлять по мере продвижения — не архив решений (архитектурные решения фиксируются в `.claude/skills/school-project-conventions/SKILL.md`), а именно "что сделано / что в работе / что дальше".

## Стек (зафиксировано)
- Backend: Python (Django/FastAPI)
- DB: PostgreSQL
- Инфраструктура: Docker + nginx, Terraform на GCP
- CI/CD: GitHub Actions
- Языки сайта: ru / en / hy (русский, английский, армянский)
- Роли: teacher, student, guest

## Сделано
- [x] Скилл `school-project-conventions` создан и зафиксирован
- [x] Определён стек и языки

## В работе
- [ ] Структура репозитория: `infra/`, `ci-cd/`, `frontend/` готовы (см. ниже) — все ждут появления самого бэкенда

## Сделано (продолжение)
- [x] `infra/docker-compose.yml` (app + nginx + db, изолированная сеть, healthcheck)
- [x] `infra/nginx/nginx.conf` (HTTP→HTTPS редирект, TLS, security headers, client_max_body_size под загрузку файлов)
- [x] `infra/db/init.sql` (pgcrypto, enum user_role teacher/student/guest; схему таблиц отдаём миграциям бэкенда)
- [x] Terraform: `backend.tf` (GCS remote state), `main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars.example`
- [x] `infra/.gitignore` (tfstate, tfvars, .env, nginx/certs, ключи)
- [x] Решено: деплой в GCP через **Workload Identity Federation** (не статичный ключ)
- [x] `ci-cd/docker/Dockerfile` (multi-stage python:3.12-slim, non-root `app`, миграции перед gunicorn)
- [x] `ci-cd/.github/workflows/deploy.yml`: lint/test → build+push (Artifact Registry) → terraform plan (PR) / apply (main) → deploy по SSH. Все actions запинены на SHA (проверено через GitHub API на 2026-09-05)

## Сделано (frontend)
- [x] `frontend/` — React (Vite), структура по доменам (`features/{courses,grades}/{teacher,student}`, `schedule/` без ролей, `users/` — логин)
- [x] i18n: react-i18next, `locales/{ru,en,hy}/common.json`, дефолт ru / fallback en
- [x] Валидация логина на латиницу на фронте (`shared/ui/validators.js`) — regex `^[a-zA-Z0-9_.-]+$`, синхронно с `infra/db/init.sql`
- [x] `frontend/Dockerfile` (multi-stage: node build → non-root nginx на 8080, `nginx.static.conf` с SPA fallback на `index.html`)
- [x] `infra/nginx/nginx.conf`: `/api/` → backend (`app:8000`), `/` → `frontend:8080`
- [x] `infra/docker-compose.yml`: добавлен сервис `frontend`, `.env.example` дополнен `FRONTEND_IMAGE`/`FRONTEND_IMAGE_TAG`

## Сделано (backend)
- [x] Скелет Django (выбран, не FastAPI): `manage.py`, `config/{settings,urls,wsgi}.py`, `requirements.txt`, `requirements-dev.txt` (ruff+pytest+pytest-django), `pyproject.toml`
- [x] Доменные модули `apps/{users,courses,grades,schedule}`, роль — вторичное разбиение внутри домена (`teacher.py`/`student.py`/`guest.py`), `schedule` — без ролей (read-only для всех)
- [x] `AUTH_USER_MODEL = users.User`, поле `role` (teacher/student/guest), `username` валидируется тем же regex `^[a-zA-Z0-9_.-]+$`, что и `frontend/src/shared/ui/validators.js` и `infra/db/init.sql` (общий валидатор — `apps/common/validators.py`)
- [x] `Course.slug` — тот же Latin-only валидатор; `title_ru/title_en/title_hy` — per-language колонки для пользовательского контента (не translation-файлы), per school-project-conventions
- [x] Роутинг по префиксам `/api/teacher/`, `/api/student/`, `/api/guest/`, `/api/schedule/`; проверка роли — на уровне middleware (`apps/common/middleware.py`), а не только во view
- [x] i18n на бэкенде: `LANGUAGE_CODE=ru`, `LANGUAGES=[ru,en,hy]`, `LocaleMiddleware`; фолбэк реализован через msgid на английском в коде + `locale/ru`, `locale/hy` каталоги (en не нужен — msgid и есть английский)
- [x] Начальные миграции сгенерированы и проверены (`migrate` на sqlite прошёл чисто) для всех 4 доменов
- [x] `ruff check .` проходит чисто (миграции исключены из линтера как автогенерируемые)
- [x] Корневой `.gitignore` добавлен (`__pycache__`, `.ruff_cache`, venv, `*.mo`)
- [x] `infra/docker-compose.yml` и `infra/.env.example`: добавлена `DJANGO_ALLOWED_HOSTS` (без неё Django с `DEBUG=false` отвечал бы 400 на все запросы)

## Сделано (guest→student→teacher флоу, по требованию пользователя)
- [x] `apps/users/guest.py`: добавлен `RegisterView` (POST `/api/guest/users/register/`) — новый аккаунт всегда `role=guest`
- [x] `apps/users/teacher.py`: `PendingGuestsView` (список только что зарегистрированных guest) + `AssignGuestView` (POST, назначает guest в класс → `role=student`, `course.students.add()`) — единственное место, где роль меняется
- [x] `Course` переиспользован как "класс" (уже был teacher+students M2M) — отдельного домена `classes` не заводили, чтобы не дублировать сущность
- [x] `apps/courses/teacher.py`: `TeacherCourseListView` дополнен `POST` (создание класса) + новый `TeacherCourseStudentsView` (список учеников по классу)
- [x] Новый домен `apps/homework/` (models/teacher.py/student.py/urls.py) — учитель создаёт ДЗ по классу, студент видит ДЗ только своего класса (`course__students=request.user`)
- [x] Миграции проверены реальным Django 5.1 в одноразовом venv: `makemigrations`/`migrate`/`check` — чисто; venv и sqlite удалены после проверки
- [x] Полный smoke-test через `curl` живого dev-сервера: register → teacher login → 403 на чужих ролях → создание класса → assign guest→student → создание ДЗ → студент видит своё ДЗ — весь цикл отработал
- [x] Найден и исправлен реальный баг: `json.loads(request.body)` кидает `UnicodeDecodeError` (не `JSONDecodeError`) на невалидных байтах → 500 вместо 400; исправлено во всех JSON-view (`guest.py`, `apps/users/teacher.py`, `apps/courses/teacher.py`, `apps/homework/teacher.py`)
- [x] Удалена пустая заглушка `apps/classes/` (создал по инерции до того, как понял, что `Course` уже покрывает "класс")
- [x] Frontend: `shared/api/AuthContext.jsx` (сессионная кука + client-side echo роли в sessionStorage, т.к. `/api/*/me` пока нет), `shared/ui/ProtectedRoute.jsx`
- [x] Frontend-страницы: `features/users/{Login,Register,PendingPage,roleHome}.jsx`, `features/homework/student/StudentHomework.jsx`, `features/admin/TeacherAdmin.jsx` (кросс-доменная админка: pending guests + assign, создание класса, ростер по классу, создание ДЗ)
- [x] Все новые UI-строки добавлены в `locales/{ru,en,hy}/common.json`

## Сделано (реальный деплой в GCP, проект vibecoding-499316)
- [x] Подтверждено с пользователем: проект `vibecoding-499316` (billing включён), новый SSH-ключ, новый GCS-бакет — все три "да"
- [x] Сгенерирован SSH-ключ `~/.ssh/school_site_deploy` (ed25519, без пароля)
- [x] Создан GCS-бакет `school-site-tfstate` (регион europe-west1, versioning on) для terraform remote state
- [x] `infra/terraform/terraform.tfvars` заполнен реальными значениями (git-ignored, не в репо). `allowed_ssh_ranges` = `35.235.240.0/20` (диапазон Google IAP, а не "IP админа" — потому что деплой из CI/CD идёт через `google-github-actions/ssh-compute` поверх IAP-туннеля)
- [x] `terraform init/plan/apply` выполнены реально — 6 ресурсов создано: VPC, subnet, 2 firewall (`allow-http-https`, `allow-ssh`), статический IP, VM `school-site-prod`
- [x] **Результат: VM живая**, внешний IP `34.38.121.190`, зона `europe-west1-b`

## Дальше (backlog) — до реально работающего сайта на этом IP ещё не хватает
- [ ] На VM (COS-образ) нужно проверить/поставить `docker compose` плагин и разложить `infra/` (docker-compose.yml, nginx/, .env) в `/opt/school-site/infra` — сейчас там ничего нет, `deploy.yml`'s `docker compose pull && up -d` упадёт без этого. SSH на VM заблокирован авто-режим-классификатором в этой сессии — это должен сделать пользователь (или отдельная сессия с явным разрешением на SSH)
- [ ] Образы `school-site-backend`/`school-site-frontend` ещё не собраны и не запушены в Artifact Registry — нужен репозиторий `school-site` в Artifact Registry (сейчас его нет)
- [ ] WIF (Workload Identity Federation) pool/provider и deploy service account в GCP — ещё не настроены; без них `ci-cd/.github/workflows/deploy.yml` не сможет аутентифицироваться
- [ ] GitHub Secrets (`GCP_PROJECT_ID=vibecoding-499316`, `GCP_WIF_PROVIDER`, `GCP_DEPLOY_SA_EMAIL`, `GCP_DEPLOY_SSH_PRIVATE_KEY` = содержимое `~/.ssh/school_site_deploy`, `GCP_DEPLOY_SSH_PUBLIC_KEY`) — не добавлены
- [ ] `ci-cd/docker/Dockerfile` собирается из корня репозитория (`context: .`), но бэкенд перенесён в `backend/` параллельным процессом — Dockerfile/workflow нужно свериup с новым расположением, иначе сборка образа сломается
- [ ] TLS-сертификаты для `infra/nginx/certs/` всё ещё не сгенерированы
- [ ] `ci-cd/.github/workflows`: добавить шаг сборки и пуша `frontend`-образа (сейчас пайплайн знает только про backend-образ)
- [ ] Реальная аутентификация в `apps/users/guest.py` — сейчас голый `django.contrib.auth`, сессии; нет rate-limit/CSRF-стратегии для API (`csrf_exempt`, это временно и небезопасно для прода)
- [ ] Нет эндпоинта `/api/*/me` — роль на фронте берётся из ответа login/register и живёт в `sessionStorage`; после ручного обновления страницы без relogin данные не протухают, но и не проверяются повторно сервером до следующего запроса к защищённому эндпоинту
- [ ] npm install/build фронтенда не прогонялся (нет сети в этой сессии) — стоит собрать перед первым деплоем и проверить в браузере
- [ ] Наполнить `locale/ru/LC_MESSAGES/django.po` и `locale/hy/...` реальными переводами (сейчас только пустые `.gitkeep`-каталоги)
- [ ] Написать тесты (pytest-django настроен, но тестов пока нет — особенно стоит покрыть guest→student assign и ролевые 403)
- [ ] `infra/nginx/certs/`: сгенерировать/подложить TLS-сертификаты (сейчас nginx.conf их ждёт, но каталог пуст и в .gitignore)
- [ ] Настроить в GCP: WIF pool/provider, deploy service account с ролями на Artifact Registry/Compute/Storage(tfstate), Artifact Registry репозиторий `school-site`
- [ ] Добавить в GitHub Secrets: `GCP_PROJECT_ID`, `GCP_WIF_PROVIDER`, `GCP_DEPLOY_SA_EMAIL`, `GCP_DEPLOY_SSH_PRIVATE_KEY`, `GCP_DEPLOY_SSH_PUBLIC_KEY` — без них workflow не запустится

## Открытые вопросы
- (пока нет)
