"use client";

import { useCurrentUser } from "@/contexts/user-context";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  const user = useCurrentUser();

  return (
    <>
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Welcome{user ? `, ${user.first_name}` : ""}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          You&apos;re signed in to the Launchbase platform console.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
            <CardDescription>Member since</CardDescription>
            <CardTitle className="text-base">
              {user
                ? new Date(user.created_at).toLocaleDateString(undefined, {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })
                : "—"}
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Account creation date
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Next step</CardDescription>
            <CardTitle className="text-base">Build your console</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Add pages under{" "}
            <code className="rounded bg-muted px-1 py-0.5 font-mono text-xs">
              app/(main)
            </code>{" "}
            and nav links in the sidebar.
          </CardContent>
        </Card>
      </div>
    </>
  );
}
