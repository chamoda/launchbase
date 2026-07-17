"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Eye, EyeOff, Lock, LogIn, Mail, ShieldCheck } from "lucide-react";
import { auth } from "@/api/endpoints/auth/auth";
import { applyApiErrorToForm } from "@/lib/api-error";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

const loginSchema = z.object({
  email: z.string().min(1, "Email is required").email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function Login() {
  const [loginError, setLoginError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();
  const queryClient = useQueryClient();

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
    // Validate a field only after it's blurred once, then re-validate live as
    // the user corrects it — so errors never flash while still typing.
    mode: "onTouched",
  });

  const loginMutation = useMutation({
    mutationFn: (data: LoginFormData) => auth(data),
    onSuccess: () => {
      setLoginError("");
      // Clear cached data so no prior session leaks into the new one.
      queryClient.clear();
      router.push("/");
    },
    onError: (error: unknown) => {
      // Field-specific problems (e.g. a malformed email) attach inline; a bad
      // credentials 401 has no field and comes back as the form-level message.
      const formError = applyApiErrorToForm(error, form.setError, {
        fields: ["email", "password"],
        fallback: "Login failed. Please try again.",
      });
      setLoginError(formError ?? "");
    },
  });

  const onSubmit = (data: LoginFormData) => {
    setLoginError("");
    loginMutation.mutate(data);
  };

  return (
    // The admin console is an internal tool, so its sign-in deliberately
    // diverges from the customer-facing login: a forced-dark, utilitarian
    // "restricted access" surface that makes the context unmistakable. We pin
    // `dark` here (rather than following theme) so the look is consistent for
    // everyone regardless of their console theme preference.
    <div className="dark flex min-h-screen items-center justify-center bg-background text-foreground p-6">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center gap-5 text-center">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-muted/60 px-3 py-1 font-mono text-[11px] font-medium uppercase tracking-widest text-muted-foreground">
            <ShieldCheck className="size-3.5 text-[#FF4F1F]" />
            Internal · Restricted
          </span>
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">
              Admin console
            </h1>
            <p className="mt-1.5 text-sm text-muted-foreground">
              Sign in with your staff credentials.
            </p>
          </div>
        </div>

        <div className="rounded-xl border bg-card p-6 shadow-sm">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <div className="relative">
                        <Mail className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                        <Input
                          type="email"
                          placeholder="you@example.com"
                          className="h-11 pl-9"
                          autoComplete="email"
                          {...field}
                        />
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <div className="relative">
                        <Lock className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                        <Input
                          type={showPassword ? "text" : "password"}
                          placeholder="Password"
                          className="h-11 pl-9 pr-9"
                          autoComplete="current-password"
                          {...field}
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword((v) => !v)}
                          disabled={!field.value?.length}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground transition-colors hover:text-foreground disabled:pointer-events-none disabled:opacity-40"
                          aria-label={
                            showPassword ? "Hide password" : "Show password"
                          }
                        >
                          {showPassword ? (
                            <EyeOff className="size-4" />
                          ) : (
                            <Eye className="size-4" />
                          )}
                        </button>
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {loginError && (
                <div className="rounded-md border border-destructive/20 bg-destructive/10 p-3 text-center text-sm text-destructive">
                  {loginError}
                </div>
              )}

              <Button
                type="submit"
                className="h-11 w-full text-sm"
                disabled={loginMutation.isPending || !form.formState.isValid}
              >
                <LogIn className="size-4" />
                {loginMutation.isPending ? "Signing in..." : "Sign in"}
              </Button>
            </form>
          </Form>
        </div>
      </div>
    </div>
  );
}
