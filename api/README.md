# Launchbase API

The Launchbase backend — a SaaS-shaped Python service built on FastAPI.

## What's in the box

- **FastAPI** with a sub-app mount pattern (`/platform`) and per-app OpenAPI docs
- **Async-first** request path — SQLAlchemy 2.x async, `asyncpg`, `httpx`
- **Postgres 16** with **Alembic** migrations (autogenerate-friendly)
- **Auth** — `argon2-cffi` password hashing, JWT via `PyJWT`, secure cookies. Endpoints: `POST /auth` (login), `POST /logout`, `GET /users/me`
- **Pagination** via `fastapi-pagination`
- **Custom CLI** — `manage.py` powered by Typer
- **Tests** — `pytest`, `pytest-asyncio`, real Postgres in CI via `testcontainers`
- **Tooling** — `uv` for env & deps, `ruff` + `pyright` (via the repo-root `pre-commit`), GitHub Actions for CI

## Requirements

- Python 3.12
- Postgres 16
- [uv](https://docs.astral.sh/uv/)

## Quick start

Instructions assume Ubuntu 24.04.

From the repo root:

```bash
cd api
uv sync                                  # create venv + install deps (incl. dev group)
cp .env.example .env                     # then edit values
createdb launchbase                      # or use psql / pgAdmin
uv run alembic upgrade head              # apply migrations
uv run fastapi dev                       # http://localhost:8000
```

Git hooks are managed at the repo root — see the [root README](../README.md#git-hooks).

Platform API docs: <http://localhost:8000/platform/docs>

## Common workflows

### Run the dev server
```bash
uv run fastapi dev
```

### Run tests
```bash
uv run pytest
```
Tests spin up Postgres in a container via `testcontainers` — no manual DB setup needed.

### Create a migration
```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

### Run a custom management command
```bash
uv run python manage.py --help
```

### Lint & type-check
From the repo root:
```bash
uv run --project api pre-commit run --all-files
```
