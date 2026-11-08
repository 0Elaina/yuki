export const CLIENT_ERROR_CODE = {
  network: 'NETWORK_ERROR',
  timeout: 'TIMEOUT',
  canceled: 'CANCELED',
  http: 'HTTP_ERROR',
  invalidResponse: 'INVALID_RESPONSE',
} as const;

export interface ApiErrorInit {
  code: string;
  message: string;
  status?: number;
  cause?: unknown;
}

export class ApiError extends Error {
  readonly code: string;
  readonly status?: number;

  constructor(init: ApiErrorInit) {
    super(init.message, { cause: init.cause });
    this.name = 'ApiError';
    this.code = init.code;
    this.status = init.status;
  }
}

export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}
