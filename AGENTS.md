# AGENTS.md

## What this project is
Django 5.x study-planning web app (SQLite, server-rendered templates, minimal JS). 8 apps: `dashboard`, `accounts`, `academics`, `planner`, `practice`, `revision`, `assistant`, `progress`, `gamification`.

**Read `StudyMate_README.md` first** — it's the product plan AND the build roadmap (master build order, per-feature prompts, Definition of Done, one-safe-step rule, commit conventions). Follow its prompts in order; implement exactly one roadmap step per session, then stop.

## Commands
- Interpreter: `venv\Scripts\python.exe` (Python 3.12). `manage.py` everywhere below.
- Check: `python manage.py check`
- Migrate: `python manage.py makemigrations` then `python manage.py migrate`
- Tests: `python manage.py test` (per app: `python manage.py test <app>`) — Django's default runner, no pytest/lint/formatter/CI configured yet.
- Dev server: `python manage.py runserver` → view at http://127.0.0.1:8000/
- Verify before/after every change: `manage.py check` + tests.

## Config / env
- Settings in `config/settings.py` (module `config`), read via `python-decouple` `config()` from `.env`. Copy `.env.example` → `.env` (SECRET_KEY, DEBUG, ALLOWED_HOSTS). Never commit `.env`.
- ALLOWED_HOSTS is `localhost,127.0.0.1`; the Django test runner's host is `testserver` — a `manage.py shell` Django `test client` must pass `HTTP_HOST='localhost'` or it 400s (`manage.py test` is unaffected).
- SQLite at `db.sqlite3` (gitignored). Timezone `Asia/Kolkata`. Templates in `templates/`, CSS design system in `static/css/styles.css`.

## Routing / wiring (don't break these)
- `config/urls.py` includes: `dashboard`, `accounts`, `academics`, `planner`, `practice`, `revision`, `assistant`. `progress` and `gamification` are in `INSTALLED_APPS` but have **no `urls.py`/namespace** — no `{% url 'progress:...' %}` / `{% url 'gamification:...' %}` yet.
- `dashboard`: **`/` is the public landing page** (`dashboard:landing`); it 302→`dashboard:home` (`/dashboard/`) when authenticated. Keep `/` as the landing.
- `templates/base.html` nav branches on `user.is_authenticated`. App templates live in `templates/<app>/`; auth templates in `templates/registration/`.
- `accounts/` = Django built-in auth views (login/logout) + `register` (UserCreationForm). No custom `User`; no `StudentProfile` yet.

## Conventions
- Enforce server-side per-student ownership on every view/model; never let one user read/modify another's data.
- AI calls only behind `assistant/` service boundary; never in views/templates; never expose API keys to the browser.
- No new dependency without justification; prefer server-rendered Django over JS frameworks.
- Generic model-driven data only — never hard-code student data.
- Add tests for models, services, views, permissions, regressions. Keep migrations clean.
- Conventional commits: `feat:`, `fix:`, `test:`, `refactor:`, `chore:`, `docs:`.

## Roadmap checkpoint
| Phase | Step | Status |
|---|---|---|
| 0 Foundation | Project structure, Django setup, settings, base layout, health check, test infra, git hygiene | ✅ Done (commits `815e5a2`, `9970f87`) |
| — | Public landing page at `/` | ✅ Done (`9970f87`) |
| 1 Accounts | Registration + login/logout | ✅ Done |
| 1 Accounts | **Student profile (PROMPT 06)** | ⏭️ NEXT |
| 1 Accounts | Profile editing (PROMPT 06) | ⬜ |
| 2 Academics | Subject → Chapter → Topic hierarchy (PROMPT 07) | ⬜ |
| … | Continue per `StudyMate_README.md` master order | ⬜ |

## NEXT STEP handoff — Student Profile (PROMPT 06)
Implement **one** roadmap step: a `StudentProfile` model linked 1:1 to the authenticated `User`.

- Model fields (Profile in `accounts/models.py`): display name, grade, board, academic year, goal, preferred daily study minutes.
- `Signal`/`get_or_create` so every registered user gets a profile (one-way: User → StudentProfile).
- Views: profile setup, profile edit, profile display (`accounts/views.py` + urls + templates in `templates/accounts/`), each enforcing the current user's own profile only.
- Do NOT add subjects yet (that's PROMPT 07).
- Migrations: `makemigrations accounts` + `migrate`.
- Tests: model + view + permission (user B can't read/edit user A's profile).
- DoD: `manage.py check` clean, `manage.py test` green, commit with convention (suggested: `feat: add student profiles`), push to `main`, update the checkpoint table above, stop.

## Git / GitHub
- Remote: `https://github.com/CodeWithAli51/StudyMate` (`origin`, branch `main`). Keep local == remote == `9970f87`.
- Only commit/push when the user asks or per roadmap step completion.