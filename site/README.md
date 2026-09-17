# Launchbase Site

The Launchbase landing page — a [TanStack Start](https://tanstack.com/start)
marketing site, statically generated and API-less. Unlike
[`platform/`](../platform/README.md), there is no orval-generated API client
here; it's just static pages and the full
[shadcn/ui](https://ui.shadcn.com) component library.

> The default `src/routes/index.tsx` is a placeholder starter — delete it and
> build your real landing page. The shadcn/ui components under
> `src/components/ui/` are pre-installed so you can move fast.

## Architecture

Built on the **Jamstack architecture** using TanStack Start's static
prerendering. Every route is rendered to HTML at build time (`prerender` in
`vite.config.ts`), so the site deploys as plain files to a CDN — fast, secure,
and cheap to host. `crawlLinks` follows internal links from rendered pages, so
a new route linked from an existing page is prerendered automatically.

## Getting Started

**Requires Node.js 24+** (current Active LTS). Use `nvm use` to pick up the
version from `.nvmrc`.

```bash
npm install
make run                                  # http://localhost:3000
```

`make run` starts the Vite dev server on port 3000 (the api runs on 8000,
`platform/` on 3001, `internal/` on 3002).

## Routing

Routes are files under `src/routes/`, and the route tree
(`src/routeTree.gen.ts`) is generated from them — by the Vite plugin during
`dev`/`build`, or on demand with `npm run routes`. It is generated output and
is not committed.

```
src/routes/__root.tsx    document shell: <html>, <head> meta, stylesheet links
src/routes/index.tsx     /
```

Page metadata lives in a route's `head()` (the equivalent of the Next.js
`metadata` export):

```tsx
export const Route = createFileRoute("/pricing")({
  head: () => ({ meta: [{ title: "Pricing" }] }),
  component: Pricing,
});
```

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
[pre-commit](https://pre-commit.com) at the repo root — oxfmt, oxlint, and
`tsc` run automatically on staged `site/` files before each commit. See the
[root README](../README.md#git-hooks) for setup.

Linting and formatting use the [oxc](https://oxc.rs) toolchain (same org as
Vite and Rolldown) rather than ESLint and Prettier: `oxlint` reads
`.oxlintrc.json`, `oxfmt` reads `.oxfmtrc.json`. Both are Rust binaries with no
plugin dependencies — a full lint of `site/` runs in ~70ms against ESLint's
~5s. The oxfmt config was migrated from the old `.prettierrc` and produces
byte-identical output, so nothing was reformatted in the switch. `platform/`
and `internal/` use the same toolchain.

Run the checks manually:

```bash
npm run lint:fix       # lint and fix
npm run format         # format all files
npm run type-check     # generate routes + tsc --noEmit
npm run validate       # type-check + lint + format:check
```

## Production

```bash
make build             # -> dist/client/
```

### Cloudflare Static Hosting

Like `platform/`, this template is optimized for deployment on **Cloudflare
Pages**. Publish the `dist/client/` directory — it contains the prerendered
HTML plus hashed assets, with no server component.
