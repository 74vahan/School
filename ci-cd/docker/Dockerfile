# syntax=docker/dockerfile:1

# --- build stage: full toolchain, compiles wheels ---
FROM python:3.12-slim AS build

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- final stage: slim runtime, no compilers, non-root ---
FROM python:3.12-slim AS final

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 gettext \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app && useradd --system --gid app --no-create-home app

WORKDIR /app

COPY --from=build /install /usr/local
COPY --chown=app:app . .

# Compiles locale/{ru,hy}/LC_MESSAGES/django.po into .mo — needed at runtime
# for gettext, but manage.py always loads settings.py, which requires these
# env vars; dummy values are fine since compilemessages never touches the DB.
RUN DJANGO_SECRET_KEY=build DATABASE_URL=sqlite:///build.sqlite3 \
    python manage.py compilemessages

USER app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings

EXPOSE 8000

# Runs migrations before serving so a fresh deploy never skips a pending migration.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
