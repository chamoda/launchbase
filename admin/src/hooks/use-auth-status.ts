"use client";

import { usePathname } from "next/navigation";
import { useUser } from "@/contexts/user-context";
import { PUBLIC_ROUTES } from "@/lib/routes";

// Single source of truth for auth status across all components.
export function useAuthStatus() {
  const { isLoading, isAuthenticated } = useUser();
  const pathname = usePathname();

  // Route-based authentication: (main) requires auth, (meta) doesn't.
  const isMetaRoute = PUBLIC_ROUTES.some((route) => pathname.startsWith(route));
  const isMainRoute = !isMetaRoute;

  const shouldShowLoader = isMainRoute && (isLoading || !isAuthenticated);

  return {
    isLoading,
    isAuthenticated,
    isMainRoute,
    isMetaRoute,
    shouldShowLoader,
  };
}
