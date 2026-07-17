"use client";

import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { useUserDelete } from "@/api/endpoints/users/users";
import type { AdminUserResponse } from "@/api/model";
import { getApiErrorMessage } from "@/lib/api-error";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface DeleteUserDialogProps {
  user: AdminUserResponse | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function DeleteUserDialog({
  user,
  open,
  onOpenChange,
}: DeleteUserDialogProps) {
  const queryClient = useQueryClient();

  const mutation = useUserDelete({
    mutation: {
      onSuccess: async () => {
        await queryClient.invalidateQueries({ queryKey: ["/users"] });
        toast.success("User deleted");
        onOpenChange(false);
      },
      onError: (error) =>
        toast.error(getApiErrorMessage(error, "Failed to delete user")),
    },
  });

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete user?</AlertDialogTitle>
          <AlertDialogDescription>
            This permanently deletes{" "}
            <span className="font-medium text-foreground">
              {user ? `${user.first_name} ${user.last_name}` : ""}
            </span>{" "}
            ({user?.email}). This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={mutation.isPending}>
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction
            variant="destructive"
            disabled={mutation.isPending}
            onClick={(event) => {
              // Keep the dialog open until the request settles.
              event.preventDefault();
              if (user) {
                mutation.mutate({ userId: user.id });
              }
            }}
          >
            {mutation.isPending ? "Deleting..." : "Delete"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
