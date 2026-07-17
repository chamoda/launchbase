"use client";

import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useGetCurrentUser } from "@/api/endpoints/users/users";
import { PUBLIC_ROUTES } from "@/lib/routes";

// Resolves the current session from GET /users/me (authenticated via the
// httponly access_token cookie) and redirects to /login when a protected
// (main) route is hit without a valid session.
export function useAuth() {
  const router = useRouter();
  const pathname = usePathname();
  const [isInitialMount, setIsInitialMount] = useState(true);

  const {
    data: user,
    isLoading: queryLoading,
    error,
    refetch,
  } = useGetCurrentUser({
    query: {
      retry: false,
      staleTime: 0,
      gcTime: 0,
    },
  });

  useEffect(() => {
    if (!queryLoading) {
      if (error) {
        // Only redirect to login from protected routes; (meta) routes such as
        // /login are public and must render without a session.
        const isMetaRoute = PUBLIC_ROUTES.some((route) =>
          pathname.startsWith(route)
        );

        if (!isMetaRoute) {
          router.replace("/login");
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
  }, [queryLoading, error, router, pathname]);

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
