/// <reference types="vite/client" />

// Public build-time config. Vite inlines `VITE_`-prefixed vars from .env;
// declaring them here keeps `import.meta.env` typed under
// `noPropertyAccessFromIndexSignature`.
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
