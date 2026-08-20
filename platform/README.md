# Launchbase Platform

The Launchbase frontend — a [TanStack Start](https://tanstack.com/start)
single-page app.

## Architecture

The app runs in TanStack Start's **SPA mode**: routes are never rendered on
the server. The build prerenders the document shell once to
`dist/client/_shell.html`; the host serves that file for every path (see
`public/_redirects`) and the router takes over on the client. That keeps
deployment to static files on a CDN, with no server runtime, while every
screen stays behind the session check in `AuthGuard`.

### Routing

Routes are files under `src/routes/`, and the route tree
(`src/routeTree.gen.ts`) is generated from them — by the Vite plugin during
`dev`/`build`, or on demand with `npm run routes`. It is generated output and
is not committed.

```
src/routes/__root.tsx          document shell + query/user providers
src/routes/login.tsx           /login          (public)
src/routes/_main.tsx           auth guard + sidebar chrome (pathless)
src/routes/_main/index.tsx     /               -> redirects to /dashboard
src/routes/_main/dashboard.tsx /dashboard
```

`_main` is a **pathless layout route**: it does not appear in the URL, but
everything nested under it renders inside the sidebar chrome and behind the
auth guard. Add a protected page by dropping a file in `src/routes/_main/`
and a nav entry in `src/components/dashboard/sidebar.tsx`. Public pages go
next to `login.tsx` and get listed in `src/lib/routes.ts`.

## Getting Started

**Requires Node.js 24+** (current Active LTS). Use `nvm use` to pick up the version from `.nvmrc`.

First, copy the env file and run the development server:

```bash
cp .env.example .env.local                      # then edit values
make run                                  # http://localhost:3001
```

## API SDK

The typed API client in `src/api/` is generated with
[orval](https://orval.dev) from the FastAPI OpenAPI spec:

- `src/api/endpoints/` — TanStack Query hooks (split per OpenAPI tag), calling
  the shared fetch client in `src/lib/api-client.ts`
- `src/api/model/` — TypeScript models
- `src/api/zod/` — standalone zod schemas for request/response/params,
  composable with react-hook-form via `@hookform/resolvers`

Regenerate after changing the API (requires the API dev server running at
`http://localhost:8000`):

```bash
npm run generate
```

Generated files are committed; don't edit them by hand.

### Forms

Forms use [react-hook-form](https://react-hook-form.com) with `zodResolver`.
Extend the generated zod schema with UI-facing validation messages while
staying anchored to the API contract:

```tsx
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { AuthBody } from "@/api/zod/auth/auth.zod";

const loginSchema = AuthBody.extend({
  email: z.string().email("Invalid email address"),
});

const form = useForm<z.infer<typeof loginSchema>>({
  resolver: zodResolver(loginSchema),
});
```

## Code Quality

Git hooks for the whole monorepo are managed by
[pre-commit](https://pre-commit.com) at the repo root — prettier, ESLint, and
`tsc` run automatically on staged `platform/` files before each commit. See the
[root README](../README.md#git-hooks) for setup.

### Manual Commands

You can also run these commands manually:

```bash
# Lint and fix issues
npm run lint:fix

# Format all files
npm run format

# Check formatting without changes
npm run format:check

# Type check
npm run type-check
```

### TypeScript Strict Mode

This project uses **maximum strictness** TypeScript configuration for enhanced type safety.

## Production

```bash
make build             # -> dist/client/
```

### Cloudflare Static Hosting

This template is optimized for deployment on **Cloudflare Pages**. Publish the
`dist/client/` directory. `public/_redirects` ships the SPA fallback rule that
serves `_shell.html` for every path, so deep links like `/dashboard` resolve.
