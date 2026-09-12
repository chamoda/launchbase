.PHONY: run revision upgrade

run:
	uv run fastapi dev --reload-dir app

migrate:
	uv run alembic revision --autogenerate

upgrade:
	uv run alembic upgrade head
