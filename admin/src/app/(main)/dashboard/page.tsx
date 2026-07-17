"use client";

import Link from "next/link";
import { useCurrentUser } from "@/contexts/user-context";
import { useUserList } from "@/api/endpoints/users/users";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  const user = useCurrentUser();
  // Cheapest possible page (limit 1) — we only need the total count here.
  const { data: users } = useUserList({ limit: 1, offset: 0 });

  return (
    <>
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Welcome{user ? `, ${user.first_name}` : ""}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          You&apos;re signed in to the Launchbase admin console.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardDescription>Total users</CardDescription>
            <CardTitle className="text-2xl">
              {users ? users.total.toLocaleString() : "—"}
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            <Link href="/users" className="underline underline-offset-4">
              Manage users
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Signed in as</CardDescription>
            <CardTitle className="text-base">
              {user ? `${user.first_name} ${user.last_name}` : "—"}
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            {user?.email ?? "—"}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Role</CardDescription>
            <CardTitle className="text-base">Administrator</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Full access to user management.
          </CardContent>
        </Card>
      </div>
    </>
  );
}
