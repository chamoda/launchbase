import type { FieldValues, Path, UseFormSetError } from "react-hook-form";
import { ApiError } from "@/lib/api-client";

// The API renders every error in FastAPI's validation-error shape:
//   { detail: [{ type, loc: ["body", <field>], msg }] }
// so a single code path handles native 422 validation errors and our custom
// business errors (409 conflict, 404 not found, ...) alike.
interface ValidationErrorItem {
  loc?: (string | number)[];
  msg?: string;
  type?: string;
}
interface ApiErrorBody {
  detail?: ValidationErrorItem[];
}

// `loc` tags where in the request the error sits; the field name follows it.
const LOCATION_TAGS = new Set(["body", "query", "path", "header", "cookie"]);

// Derive the offending field from a `loc` array, e.g. ["body", "email"] ->
// "email". Returns null for form-level errors whose loc carries no field
// (e.g. ["body"] on a 401).
function fieldFromLoc(loc: ValidationErrorItem["loc"]): string | null {
  if (!loc) return null;
  for (let i = loc.length - 1; i >= 0; i--) {
    const part = loc[i];
    if (typeof part === "string" && !LOCATION_TAGS.has(part)) return part;
  }
  return null;
}

function getDetail(error: unknown): ValidationErrorItem[] | undefined {
  if (error instanceof ApiError) {
    const detail = (error.data as ApiErrorBody | undefined)?.detail;
    if (Array.isArray(detail) && detail.length > 0) return detail;
  }
  return undefined;
}

// Pull a human-readable message out of an unknown thrown value: the API's first
// structured error message when present, otherwise a caller-supplied fallback.
// Network failures arrive as the native fetch TypeError (no response body).
export function getApiErrorMessage(error: unknown, fallback: string): string {
  const detail = getDetail(error);
  if (detail) {
    const message = detail[0]?.msg;
    if (typeof message === "string" && message.length > 0) return message;
    return fallback;
  }
  if (error instanceof TypeError) {
    return "Network error. Please check your connection and try again.";
  }
  return fallback;
}

// Apply an API error to a react-hook-form: each error whose field is one of the
// form's `fields` is attached inline (shown next to that input); anything left
// over — errors with no field, or for fields the form doesn't render — is
// returned as a single form-level message the caller can surface (banner,
// toast, ...). Returns null when every error was mapped to a field.
export function applyApiErrorToForm<T extends FieldValues>(
  error: unknown,
  setError: UseFormSetError<T>,
  options: { fields: readonly Path<T>[]; fallback: string }
): string | null {
  const detail = getDetail(error);
  if (!detail) {
    // No structured body: network error or an unexpected shape.
    return getApiErrorMessage(error, options.fallback);
  }

  const known = new Set<string>(options.fields as readonly string[]);
  let formError: string | null = null;

  for (const item of detail) {
    const message = item.msg ?? options.fallback;
    const field = fieldFromLoc(item.loc);
    if (field && known.has(field)) {
      setError(field as Path<T>, { type: "server", message });
    } else if (!formError) {
      // First error we can't attach to a field becomes the form-level message.
      formError = message;
    }
  }

  return formError;
}
