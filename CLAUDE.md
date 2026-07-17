# Launchbase

A polyglot monorepo: a FastAPI backend and three Next.js SSG-first frontends.
Each project is self-contained with its own tooling, README, and (where present)
a nested `CLAUDE.md` with deeper rules.

## Projects

| Folder      | Stack                          | Toolchain     |
| ----------- | ------------------------------ | ------------- |
| `api/`      | FastAPI, async SQLAlchemy, PG  | Python + `uv` |
| `platform/` | Next.js app (SSG-first)        | Node + `npm`  |
| `admin/`    | Next.js admin console          | Node + `npm`  |
| `site/`     | Next.js landing page (API-less)| Node + `npm`  |

`api/CLAUDE.md` holds the backend rules — read it before touching `api/`.

## Conventions

- Run Python commands through `uv` (e.g. `uv run ...`), never a bare `python`.
- The frontends target Node 24+; run `nvm use` in a frontend folder to match `.nvmrc`.
- `platform/src/api/` is a **generated** typed client (orval, from the API's
  OpenAPI spec). After backend schema/endpoint changes, regenerate it with
  `cd platform && npm run generate` — don't hand-edit generated files.
- Hooks are managed repo-wide by pre-commit; run from the root with
  `uv run --project api pre-commit run --all-files`.
