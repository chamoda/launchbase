"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { useUserCreate, useUserUpdate } from "@/api/endpoints/users/users";
import type { AdminUserResponse } from "@/api/model";
import { applyApiErrorToForm } from "@/lib/api-error";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

// Shared create/edit schema. Password is only used in create mode, where it is
// required (min 8 chars). In edit mode the field is not rendered and its value
// is ignored — passwords are changed elsewhere — so validation is relaxed to
// keep the edit form submittable.
const makeUserFormSchema = (isEdit: boolean) =>
  z.object({
    first_name: z.string().min(1, "First name is required").max(100),
    last_name: z.string().min(1, "Last name is required").max(100),
    email: z
      .string()
      .min(1, "Email is required")
      .email("Invalid email address"),
    password: isEdit
      ? z.string()
      : z
          .string()
          .min(1, "Password is required")
          .min(8, "Password must be at least 8 characters"),
    is_admin: z.boolean(),
    is_active: z.boolean(),
  });

type UserFormData = z.infer<ReturnType<typeof makeUserFormSchema>>;

const emptyValues: UserFormData = {
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  is_admin: false,
  is_active: true,
};

interface UserFormDialogProps {
  mode: "create" | "edit";
  user?: AdminUserResponse;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function UserFormDialog({
  mode,
  user,
  open,
  onOpenChange,
}: UserFormDialogProps) {
  const queryClient = useQueryClient();
  const isEdit = mode === "edit";

  const form = useForm<UserFormData>({
    resolver: zodResolver(makeUserFormSchema(isEdit)),
    defaultValues: emptyValues,
    mode: "onTouched",
  });

  // Reset the form each time the dialog opens so stale input from a prior use
  // never leaks in, and edit mode is seeded from the selected user.
  useEffect(() => {
    if (open) {
      form.reset(
        isEdit && user
          ? {
              first_name: user.first_name,
              last_name: user.last_name,
              email: user.email,
              password: "",
              is_admin: user.is_admin,
              is_active: user.is_active,
            }
          : emptyValues
      );
    }
  }, [open, isEdit, user, form]);

  const invalidateUsers = () =>
    queryClient.invalidateQueries({ queryKey: ["/users"] });

  // Attach field-specific errors (e.g. a duplicate-email 409) inline next to
  // the input; surface anything left over as a toast. Password isn't a field
  // in edit mode, so it's only mappable when creating.
  const handleMutationError = (error: unknown, fallback: string) => {
    const fields = isEdit
      ? (["first_name", "last_name", "email"] as const)
      : (["first_name", "last_name", "email", "password"] as const);
    const formError = applyApiErrorToForm(error, form.setError, {
      fields,
      fallback,
    });
    if (formError) toast.error(formError);
  };

  const createMutation = useUserCreate({
    mutation: {
      onSuccess: async () => {
        await invalidateUsers();
        toast.success("User created");
        onOpenChange(false);
      },
      onError: (error) => handleMutationError(error, "Failed to create user"),
    },
  });

  const updateMutation = useUserUpdate({
    mutation: {
      onSuccess: async () => {
        await invalidateUsers();
        toast.success("User updated");
        onOpenChange(false);
      },
      onError: (error) => handleMutationError(error, "Failed to update user"),
    },
  });

  const isPending = createMutation.isPending || updateMutation.isPending;

  const onSubmit = (data: UserFormData) => {
    if (isEdit && user) {
      updateMutation.mutate({
        userId: user.id,
        data: {
          first_name: data.first_name,
          last_name: data.last_name,
          email: data.email,
          is_admin: data.is_admin,
          is_active: data.is_active,
        },
      });
      return;
    }
    createMutation.mutate({
      data: {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email,
        password: data.password,
        is_admin: data.is_admin,
        is_active: data.is_active,
      },
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{isEdit ? "Edit user" : "Add user"}</DialogTitle>
          <DialogDescription>
            {isEdit
              ? "Update this user's details and access."
              : "Create a new user account."}
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-4"
            noValidate
          >
            <div className="grid grid-cols-2 gap-3">
              <FormField
                control={form.control}
                name="first_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>First name</FormLabel>
                    <FormControl>
                      <Input autoComplete="given-name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="last_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Last name</FormLabel>
                    <FormControl>
                      <Input autoComplete="family-name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input type="email" autoComplete="email" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {!isEdit && (
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input
                        type="password"
                        placeholder="At least 8 characters"
                        autoComplete="new-password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}

            <FormField
              control={form.control}
              name="is_admin"
              render={({ field }) => (
                <FormItem className="flex items-center justify-between rounded-md border p-3">
                  <div className="space-y-0.5">
                    <FormLabel>Administrator</FormLabel>
                    <FormDescription>
                      Can sign in to this admin console.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="is_active"
              render={({ field }) => (
                <FormItem className="flex items-center justify-between rounded-md border p-3">
                  <div className="space-y-0.5">
                    <FormLabel>Active</FormLabel>
                    <FormDescription>
                      Inactive users cannot use their account.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            <DialogFooter>
              <Button
                type="button"
                variant="ghost"
                onClick={() => onOpenChange(false)}
                disabled={isPending}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={isPending}>
                {isPending
                  ? "Saving..."
                  : isEdit
                    ? "Save changes"
                    : "Create user"}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
