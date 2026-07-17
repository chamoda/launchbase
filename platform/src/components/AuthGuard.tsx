"use client";

import { useAuthStatus } from "@/hooks/use-auth-status";
import FullScreenLoader from "./FullScreenLoader";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { shouldShowLoader } = useAuthStatus();

  if (shouldShowLoader) {
    return <FullScreenLoader />;
  }

  return <>{children}</>;
}
