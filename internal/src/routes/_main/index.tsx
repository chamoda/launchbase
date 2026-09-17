import { createFileRoute, redirect } from "@tanstack/react-router";

// `/` is not a page of its own — it hands off to the dashboard before any
// component renders, so there is no loader flash on the way through.
export const Route = createFileRoute("/_main/")({
  beforeLoad: () => {
    throw redirect({ to: "/dashboard" });
  },
});
