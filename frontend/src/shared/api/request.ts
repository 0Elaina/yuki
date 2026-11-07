import type { AxiosRequestConfig, Method } from 'axios'

import { ApiError, CLIENT_ERROR_CODE } from './error'
import { http } from './http'
import { type ApiResponse, SUCCESS_CODE } from './types'

export type RequestConfig = Omit<AxiosRequestConfig, 'method'> & {
  method: Method
}

/**
 * 发出请求并解包统一响应体，成功时直接返回 data。
 * 业务错误以 ApiError 抛出，由调用方决定如何处理。
 */
export async function request<T>(config: RequestConfig): Promise<T> {
  const response = await http.request<ApiResponse<T> | undefined>(config)
  const body = response.data

  if (!body || body.code !== SUCCESS_CODE) {
    throw new ApiError({
      code: body?.code ?? CLIENT_ERROR_CODE.invalidResponse,
      message: body?.message || '响应格式异常',
      status: response.status,
    })
  }

  return body.data
}
