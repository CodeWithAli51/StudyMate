# AGENTS.md

## What this project is
Django 5.x study-planning web app (SQLite, server-rendered templates, minimal JS). The app is in early scaffolding: 8 empty Django apps exist (`accounts`, `academics`, `planner`, `progress`, `practice`, `revision`, `assistant`, `gamification`, `dashboard`) but **no models or views are implemented yet**.

The authoritative product plan **and** agent build roadmap is `StudyMate_README.md`. Read it first — it defines the master build order, per-feature step prompts, a "one safe step at a time" rule, a Definition of Done, and conventional-commit message conventions. Follow its step prompts in order; the agent is expected to implement exactly one roadmap step per session and stop.

## Current state
The scaffold now passes `manage.py check`. Every app that `config/urls.py` includes has its own `urls.py` with stub `index` `TemplateView`s and matching placeholder templates under `templates/<app>/`. `accounts/` provides login/logout (Django built-in auth views) plus a `register` view using `UserCreationForm`. No apps have models yet; auth uses Django's built-in `User` (no `StudentProfile`).

Who's wired up:
- `config/urls.py` includes: `dashboard`, `accounts`, `academics`, `planner`, `practice`, `revision`, `assistant`. **Note:** `progress` and `gamification` are in `INSTALLED_APPS` but have **no `urls.py`** and no URL namespace — don't call `{% url 'progress:...' %}` / `{% url 'gamification:...' %}` until those apps get views.
- `dashboard` routing: **`/` is the public marketing landing page** (`dashboard:landing`, `LandingView`) which returns 302→`dashboard:home` for authenticated users; the authenticated home lives at `/dashboard/` (`dashboard:home`). When adding app pages, don't route the landing page away from `/`.
- `templates/base.html` is the shared layout and defines the CSS design system in `static/css/styles.css`; the nav links branch on `user.is_authenticated` (brand/Home → landing for anonymous, dashboard for logged-in). App page templates live under `templates/<app>/`.
- ALLOWED_HOSTS in `.env` is `localhost,127.0.0.1`. The Django test runner's host is `testserver`, so a standalone `manage.py shell` Django `test client` will 400 unless you pass `HTTP_HOST='localhost'`; normal `manage.py test` is unaffected.

Run `manage.py check` and the test suite before/after changes.

## Commands
- Activate venv: `venv\Scripts\activate` (or call `venv\Scripts\python.exe` directly). Python 3.12 is the interpreter.
- Install deps: `pip install -r requirements.txt`
- Django checks: `python manage.py check`
- Run migrations: `python manage.py makemigrations` then `python manage.py migrate`
- Dev server: `python manage.py runserver`
- Tests: Django's default runner — `python manage.py test` (runs a specific app with `python manage.py test <app>`). There is no pytest/config for it yet; per-app `tests.py` files exist but are empty.

## Configuration / env
- Settings live in `config/settings.py` (module name `config`), read via `python-decouple`'s `config()` from `.env`.
- Copy `.env.example` → `.env` before running. Secrets (SECRET_KEY, later AI keys) come from env, never commit them.
- DB: SQLite at `db.sqlite3` (gitignored). Timezone `Asia/Kolkata`.
- Templates in `templates/` (base design system in `templates/base.html`), static in `static/`.

## Coding / contribution conventions (from StudyMate_README.md)
- Enforce server-side per-student ownership on every view/model; never let one user read/modify another's data.
- Keep AI code behind a dedicated service boundary (`assistant/`) — never put provider/LLM calls in templates or views, never expose API keys to the browser.
- No new dependency without a justified reason; prefer Django + server-rendered HTML/CSS over frontend frameworks/JS.
- Do not hard-code student-specific data (student profiles are generic model-driven).
- Keep migrations clean; add tests for meaningful business logic (models, services, views, permissions, regressions).
- Conventional commits, e.g. `feat:`, `fix:`, `test:`, `refactor:`, `chore:`, `docs:`.
