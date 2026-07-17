# Launchbase Admin

The Launchbase admin console — a [Next.js](https://nextjs.org) app with a
special focus on SSG-first rendering. It talks to the API's `/admin` surface
(admin-audience tokens, `admin_access_token` cookie) and provides user
management for administrators.

## Architecture

This project is built on the **Jamstack architecture**, leveraging Next.js's powerful Static Site Generation (SSG) capabilities. By pre-rendering pages at build time, the application delivers:

- **Lightning-fast performance**: Static HTML files served directly from CDN
- **Enhanced security**: No server-side runtime reduces attack surface
- **Scalability**: Static files can be distributed globally with minimal infrastructure
- **SEO optimization**: Fully rendered HTML improves search engine indexing

### Next.js SSG Configuration

The project is configured with SSG-first rendering, meaning pages are generated as static HTML at build time.

## Getting Started

**Requires Node.js 24+** (current Active LTS). Use `nvm use` to pick up the version from `.nvmrc`.

First, copy the env file and run the development server:

```bash
cp .env.example .env.local                # then edit values
make run                                  # http://localhost:3002
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
`tsc` run automatically on staged `admin/` files before each commit. See the
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

### Cloudflare Static Hosting

This template is optimized for deployment on **Cloudflare Pages** as Next.js static site deployment
