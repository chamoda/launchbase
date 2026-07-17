"use client";

import { createContext, useContext, ReactNode } from "react";
import { useAuth } from "@/hooks/use-auth";
import type { AdminUserResponse } from "@/api/model";

type User = AdminUserResponse;

interface UserContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isUnauthenticated: boolean;
  error: unknown;
  refetch: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const {
    user,
    isLoading,
    isAuthenticated,
    isUnauthenticated,
    error,
    refetch,
  } = useAuth();

  return (
    <UserContext.Provider
      value={{
        user: user || null,
        isLoading,
        isAuthenticated,
        isUnauthenticated,
        error,
        refetch,
      }}
    >
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}

export function useCurrentUser() {
  const { user, isAuthenticated } = useUser();
  return isAuthenticated ? user : null;
}
