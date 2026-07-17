<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="branding/banner-dark.svg">
    <img src="branding/banner-light.svg" alt="Launchbase — a polyglot monorepo template" width="100%">
  </picture>
</p>

A polyglot monorepo template: a FastAPI backend and Next.js SSG-first
frontends, with shared tooling wired for monorepo development. Opinionated
defaults so you can skip the wiring and start building.

## Structure

| Folder      | What it is                                                                     | Setup                                     |
| ----------- | ------------------------------------------------------------------------------ | ----------------------------------------- |
| `api/`      | FastAPI backend — async SQLAlchemy, Postgres, Alembic, JWT auth, pytest        | [api/README.md](api/README.md)            |
| `platform/` | Next.js frontend — SSG-first (Jamstack), Tailwind, shadcn/ui                   | [platform/README.md](platform/README.md)  |
| `admin/`    | Next.js admin console — SSG-first, user management on the API `/admin` surface | [admin/README.md](admin/README.md)        |
| `site/`     | Next.js landing page — SSG-first, API-less, full shadcn/ui component set       | [site/README.md](site/README.md)          |

Each folder's README has the setup and workflow details — start there.

## Requirements

- Python 3.12 and [uv](https://docs.astral.sh/uv/)
- Node.js 24+ (`nvm use` inside a frontend folder picks up `.nvmrc`)
- Postgres 16

## Dev session

[tmuxp](https://tmuxp.git-pull.com/) builds the preconfigured dev session from
`.tmuxp.yaml`. Run `tmuxp load .` from the repo root.

## Git hooks

[pre-commit](https://pre-commit.com) manages hooks for the whole monorepo via
`.pre-commit-config.yaml`. Install once after cloning:

```bash
uv run --project api pre-commit install
```
