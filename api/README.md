# Launchbase API

The Launchbase backend — a SaaS-shaped Python service built on FastAPI.

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

### Create an admin user
```bash
uv run manage.py create-user \
  --first-name Admin \
  --last-name User \
  --email admin@example.com \
  --admin
```
The login password is generated and printed unless you pass `--password`.

### Run a custom management command
```bash
uv run manage.py --help
```

### Lint & type-check
From the repo root:
```bash
uv run --project api pre-commit run --all-files
```
