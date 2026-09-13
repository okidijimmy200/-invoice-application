export class ApiError extends Error {
  constructor(message: string, readonly status: number, readonly details?: unknown) {
    super(message);
  }
}

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api/v1${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const body: unknown = response.status === 204 ? undefined : await response.json();
  if (!response.ok) {
    const message = typeof body === "object" && body !== null && "message" in body
      ? String(body.message)
      : typeof body === "object" && body !== null && "detail" in body
        ? "Please correct the highlighted fields."
        : "Request failed";
    throw new ApiError(message, response.status, body);
  }
  return body as T;
}
