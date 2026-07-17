![Banner](banner.png)

This is a [Next.js](https://nextjs.org) project template with special focus on SSG first rendering.

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

First, run the development server:

```bash
npm run dev
```

## Code Quality

This project enforces code quality standards automatically using Git hooks and lint-staged:

### Pre-commit Hooks

The project uses [Husky](https://typicode.github.io/husky/) and [lint-staged](https://github.com/lint-staged/lint-staged) to run quality checks on staged files before each commit:

- **Prettier**: Automatically formats all staged files
- **ESLint**: Lints and fixes JavaScript/TypeScript files
- **Next.js lint**: Runs Next.js-specific linting rules

Configuration is defined in `.lintstagedrc.mjs` using ES module syntax.

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

This project uses **maximum strictness** TypeScript configuration for enhanced type safety:

## Production

### Cloudflare Static Hosting

This template is optimized for deployment on **Cloudflare Pages** as Next.js static site deployment
