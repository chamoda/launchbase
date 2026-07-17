# Launchbase Site

The Launchbase landing page — a [Next.js](https://nextjs.org) marketing site,
SSG-first and API-less. Unlike [`platform/`](../platform/README.md), there is
no orval-generated API client here; it's just static pages and the full
[shadcn/ui](https://ui.shadcn.com) component library.

> The default `src/app/page.tsx` is a placeholder starter — delete it and build
> your real landing page. The shadcn/ui components under `src/components/ui/`
> are pre-installed so you can move fast.

## Architecture

Built on the **Jamstack architecture** using Next.js Static Site Generation
(SSG). Pages are pre-rendered to static HTML at build time (`output: "export"`
in `next.config.ts`), so the site deploys as plain files to a CDN — fast,
secure, and cheap to host.

## Getting Started

**Requires Node.js 24+** (current Active LTS). Use `nvm use` to pick up the
version from `.nvmrc`.

```bash
npm install
cp .env.example .env.local                # then edit values (optional)
make run                                  # http://localhost:3000
```

`make run` starts the Next.js dev server on port 3000 (the api runs on 8000,
`platform/` on 3001).

## Components

The full shadcn/ui library ships under `src/components/ui/`. Import directly:

```tsx
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
```

Add or update components with the shadcn CLI as usual:

```bash
npx shadcn@latest add <component>
```

## Code Quality

Git hooks for the whole monorepo are managed by
[pre-commit](https://pre-commit.com) at the repo root — prettier, ESLint, and
`tsc` run automatically on staged `site/` files before each commit. See the
[root README](../README.md#git-hooks) for setup.

Run the checks manually:

```bash
npm run lint:fix       # lint and fix
npm run format         # format all files
npm run type-check     # tsc --noEmit
npm run validate       # type-check + lint + format:check
```

## Production

### Cloudflare Static Hosting

Like `platform/`, this template is optimized for deployment on **Cloudflare
Pages** as a Next.js static site export.
