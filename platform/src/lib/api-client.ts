// Shared fetch mutator used by all Orval-generated endpoints.
// Cookie-based auth: `credentials: "include"` sends the session cookie to the API.
// Fail at load rather than letting an unset var produce a `undefined/...`
// URL, which resolves against the dev server and 404s confusingly.
const apiUrl = import.meta.env.VITE_API_URL;
if (!apiUrl) {
  throw new Error("VITE_API_URL is not set — copy .env.example to .env.local");
}

const baseURL = `${apiUrl}/platform`;

// Error thrown for non-2xx responses: HTTP `status` and the parsed response
// `data`. Network failures (no response) surface as the native fetch
// `TypeError` instead.
export class ApiError<TData = unknown> extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public data: TData
  ) {
    super(`API request failed with status ${status}`);
    this.name = "ApiError";
  }
}

const parseBody = async (response: Response): Promise<unknown> => {
  if (response.status === 204) {
    return undefined;
  }
  const contentType = response.headers.get("content-type") ?? "";
  const text = await response.text();
  if (!text) {
    return undefined;
  }
  return contentType.includes("application/json") ? JSON.parse(text) : text;
};

// Orval `fetch` httpClient calls this with the request path and a RequestInit
// (method, headers, body, signal). We prepend the base URL, attach credentials,
// parse the body, and throw `ApiError` on non-2xx so TanStack Query treats it
// as an error.
export const customInstance = async <T>(
  url: string,
  options?: RequestInit
): Promise<T> => {
  const response = await fetch(`${baseURL}${url}`, {
    ...options,
    credentials: "include",
  });

  const data = await parseBody(response);

  if (!response.ok) {
    throw new ApiError(response.status, response.statusText, data);
  }

  return data as T;
};

export default customInstance;

// Error type surfaced on generated hooks (e.g. useQuery error is ApiError<TError>).
export type ErrorType<TError> = ApiError<TError>;

// Body type helper for generated mutation inputs.
export type BodyType<TBody> = TBody;
