import { useLocation, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { useGetCurrentInternalUser } from "@/api/endpoints/users/users";
import { PUBLIC_ROUTES } from "@/lib/routes";

// Resolves the current session from GET /users/self (authenticated via the
// httponly internal_access_token cookie) and redirects to /login when a
// protected route is hit without a valid session.
export function useAuth() {
  const navigate = useNavigate();
  const pathname = useLocation({ select: (l) => l.pathname });
  const [isInitialMount, setIsInitialMount] = useState(true);

  const {
    data: user,
    isLoading: queryLoading,
    error,
    refetch,
  } = useGetCurrentInternalUser({
    query: {
      retry: false,
      staleTime: 0,
      gcTime: 0,
    },
  });

  useEffect(() => {
    if (!queryLoading) {
      if (error) {
        // Only redirect to login from protected routes; public routes such
        // as /login must render without a session.
        const isMetaRoute = PUBLIC_ROUTES.some((route) =>
          pathname.startsWith(route)
        );

        if (!isMetaRoute) {
          navigate({ to: "/login", replace: true });
          return undefined;
        }
      }
      // Small buffer to prevent UI flash while the auth check settles.
      const timer = setTimeout(() => {
        setIsInitialMount(false);
      }, 100);
      return () => clearTimeout(timer);
    }
    return undefined;
  }, [queryLoading, error, navigate, pathname]);

  const isLoading = queryLoading || isInitialMount;
  const isAuthenticated = !isLoading && !error && !!user;
  const isUnauthenticated = !isLoading && (!!error || !user);

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    isUnauthenticated,
    refetch,
  };
}
