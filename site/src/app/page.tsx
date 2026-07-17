import {
  ArrowRight,
  Check,
  LayoutTemplate,
  Rocket,
  Server,
} from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Logo, Logomark } from "@/components/logo";

// Placeholder landing page — replace this with your marketing site.
// The full shadcn/ui component library is available under
// `@/components/ui/*` so you can build fast.

const stack = [
  {
    dir: "api/",
    icon: Server,
    title: "FastAPI backend",
    body: "Async SQLAlchemy, Postgres, Alembic migrations, JWT auth and pytest — the service, wired and ready.",
  },
  {
    dir: "platform/",
    icon: LayoutTemplate,
    title: "Next.js platform",
    body: "The SSG-first app, with Tailwind, shadcn/ui and a typed API client generated from OpenAPI.",
  },
  {
    dir: "site/",
    icon: Rocket,
    title: "Landing site",
    body: "This API-less marketing site, shipping the full shadcn/ui component set for fast page building.",
  },
];

const tech = [
  "FastAPI",
  "Next.js",
  "Postgres",
  "Tailwind",
  "shadcn/ui",
  "TypeScript",
];

const tooling = [
  "Typed API SDK generated with orval (TanStack Query + zod)",
  "pre-commit hooks: ruff & pyright, prettier, eslint & tsc",
  "tmuxp dev session — API and web servers in one command",
  "Opinionated defaults so you skip the wiring and build",
];

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center overflow-hidden px-6 py-20 font-[family-name:var(--font-geist-sans)]">
      {/* Decorative grid backdrop, fading out toward the page body. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[520px] [mask-image:radial-gradient(ellipse_60%_100%_at_50%_0%,black,transparent)]"
      >
        <div className="absolute inset-0 bg-[linear-gradient(to_right,var(--color-border)_1px,transparent_1px),linear-gradient(to_bottom,var(--color-border)_1px,transparent_1px)] bg-[size:44px_44px] opacity-60" />
      </div>

      <div className="flex w-full max-w-4xl flex-col items-center gap-14 text-center">
        {/* Hero */}
        <div className="flex flex-col items-center gap-6">
          <Logo className="h-11" />
          <Badge variant="outline" className="rounded-full bg-background/60">
            Full-stack monorepo template
          </Badge>
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-balance sm:text-6xl">
            Launch faster on a base that&apos;s{" "}
            <span className="text-[#FF4F1F]">already wired</span>
          </h1>
          <p className="max-w-xl text-balance text-lg text-muted-foreground">
            A FastAPI backend and a Next.js SSG-first frontend in one monorepo,
            with shared tooling and opinionated defaults. Skip the plumbing and
            start building your product.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-2 pt-1">
            {tech.map((t) => (
              <span
                key={t}
                className="rounded-full border bg-background/60 px-3 py-1 text-xs font-medium text-muted-foreground"
              >
                {t}
              </span>
            ))}
          </div>
        </div>

        {/* The three packages */}
        <div className="grid w-full gap-4 text-left sm:grid-cols-3">
          {stack.map(({ dir, icon: Icon, title, body }) => (
            <Card
              key={dir}
              className="gap-4 transition-colors hover:border-foreground/20"
            >
              <CardHeader className="gap-3">
                <div className="flex items-center justify-between">
                  <span className="flex size-9 items-center justify-center rounded-lg border bg-muted/40 text-foreground">
                    <Icon className="size-4.5" strokeWidth={1.75} />
                  </span>
                  <code className="rounded bg-muted px-1.5 py-0.5 font-[family-name:var(--font-geist-mono)] text-xs text-muted-foreground">
                    {dir}
                  </code>
                </div>
                <CardTitle className="text-base">{title}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">
                {body}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Quick start */}
        <div className="w-full max-w-2xl overflow-hidden rounded-xl border bg-muted/30 text-left">
          <div className="flex items-center gap-1.5 border-b bg-muted/50 px-4 py-2.5">
            <span className="size-2.5 rounded-full bg-muted-foreground/25" />
            <span className="size-2.5 rounded-full bg-muted-foreground/25" />
            <span className="size-2.5 rounded-full bg-muted-foreground/25" />
            <span className="ml-2 text-xs text-muted-foreground">
              get started
            </span>
          </div>
          <pre className="overflow-x-auto px-4 py-4 font-[family-name:var(--font-geist-mono)] text-sm leading-relaxed">
            <code>
              <span className="text-muted-foreground select-none">$ </span>
              git clone &lt;repo-url&gt; launchbase{"\n"}
              <span className="text-muted-foreground select-none">$ </span>
              cd launchbase{"\n"}
              <span className="text-muted-foreground select-none">$ </span>
              tmuxp load <span className="text-[#FF4F1F]">.</span>
              <span className="text-muted-foreground">
                {"  "}# api + web, one command
              </span>
            </code>
          </pre>
        </div>

        {/* What's already wired */}
        <ul className="grid w-full max-w-2xl gap-x-8 gap-y-3 text-left text-sm text-muted-foreground sm:grid-cols-2">
          {tooling.map((item) => (
            <li key={item} className="flex items-start gap-2.5">
              <Check
                aria-hidden
                className="mt-0.5 size-4 shrink-0 text-[#FF4F1F]"
                strokeWidth={2.5}
              />
              {item}
            </li>
          ))}
        </ul>

        {/* CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-3">
          <a
            className={buttonVariants({ size: "lg" })}
            href="https://ui.shadcn.com/docs/components"
            target="_blank"
            rel="noopener noreferrer"
          >
            Browse components
            <ArrowRight className="size-4" />
          </a>
          <a
            className={buttonVariants({ variant: "outline", size: "lg" })}
            href="https://nextjs.org/docs"
            target="_blank"
            rel="noopener noreferrer"
          >
            Next.js docs
          </a>
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-20 flex items-center gap-2 text-xs text-muted-foreground">
        <Logomark className="size-4" />
        <span>
          Edit{" "}
          <code className="rounded bg-muted px-1.5 py-0.5 font-[family-name:var(--font-geist-mono)]">
            src/app/page.tsx
          </code>{" "}
          to make it yours.
        </span>
      </footer>
    </main>
  );
}
