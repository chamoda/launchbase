import { defineConfig } from "orval";

export default defineConfig({
  // TanStack Query hooks + typed models, split per OpenAPI tag (per-domain files).
  launchbase: {
    input: "http://localhost:8000/platform/openapi.json",
    output: {
      mode: "tags-split",
      target: "src/api/endpoints",
      schemas: "src/api/model",
      client: "react-query",
      httpClient: "fetch",
      clean: true,
      override: {
        // Return just the response body (not a { data, status, headers }
        // wrapper) so hooks expose the typed payload directly.
        fetch: {
          includeHttpResponseReturnType: false,
        },
        mutator: {
          path: "src/lib/api-client.ts",
          name: "customInstance",
        },
      },
    },
  },
  // Standalone zod schemas (request/response/params), composable for react-hook-form.
  launchbaseZod: {
    input: "http://localhost:8000/platform/openapi.json",
    output: {
      mode: "tags-split",
      target: "src/api/zod",
      fileExtension: ".zod.ts",
      client: "zod",
      clean: true,
    },
  },
});
