import axios from 'axios'

import { ApiError, CLIENT_ERROR_CODE } from './error'
import { notifyError } from './notifier'
import type { ApiResponse } from './types'

const TIMEOUT_MS = 15_000

export const http = axios.create({
  baseURL: '/api/v1',
  timeout: TIMEOUT_MS,
  headers: {
    Accept: 'application/json',
  },
})

function toApiError(error: unknown): ApiError {
  if (error instanceof ApiError) {
    return error
  }

  if (axios.isCancel(error)) {
    return new ApiError({
      code: CLIENT_ERROR_CODE.canceled,
      message: '请求已取消',
      cause: error,
    })
  }

  if (axios.isAxiosError(error)) {
    if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
      return new ApiError({
        code: CLIENT_ERROR_CODE.timeout,
        message: '请求超时，请稍后重试',
        cause: error,
      })
    }

    const status = error.response?.status
    const body = error.response?.data as ApiResponse<unknown> | undefined
    const fallbackMessage = status === undefined ? '网络异常，请检查连接' : '请求失败，请稍后重试'

    return new ApiError({
      code: body?.code ?? CLIENT_ERROR_CODE.http,
      message: body?.message ?? fallbackMessage,
      status,
      cause: error,
    })
  }

  return new ApiError({
    code: CLIENT_ERROR_CODE.http,
    message: '请求失败，请稍后重试',
    cause: error,
  })
}

function shouldNotify(error: ApiError): boolean {
  if (error.code === CLIENT_ERROR_CODE.canceled) {
    return false
  }

  // 没有响应说明是网络中断或超时，用户能感知到的只有“没连上”。
  if (error.status === undefined) {
    return true
  }

  return error.status === 429 || error.status >= 500
}

http.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    const apiError = toApiError(error)

    if (shouldNotify(apiError)) {
      notifyError(apiError.message)
    }

    return Promise.reject(apiError)
  },
)
