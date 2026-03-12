import request, { type ApiResponse, type PageResponse } from '@/api'
import type { AxiosRequestConfig } from 'axios'

export async function get<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return request.get(url, config)
}

export async function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return request.post(url, data, config)
}

export async function put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return request.put(url, data, config)
}

export async function del<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return request.delete(url, config)
}

export async function getPage<T>(url: string, params?: Record<string, unknown>): Promise<PageResponse<T>> {
  const response = await request.get(url, { params })
  return response.data as PageResponse<T>
}

export { type ApiResponse, type PageResponse }