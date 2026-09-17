import { useLocation } from "@tanstack/react-router";
import { useUser } from "@/contexts/user-context";
import { PUBLIC_ROUTES } from "@/lib/routes";

// Single source of truth for auth status across all components.
export function useAuthStatus() {
  const { isLoading, isAuthenticated } = useUser();
  const pathname = useLocation({ select: (l) => l.pathname });

  // Route-based authentication: routes under _main require auth, public
  // ones (PUBLIC_ROUTES) don't.
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
