export interface User {
  id: number
  username: string
  name: string
  email?: string
  phone?: string
  avatar?: string
  status: number
  created_at: string
  updated_at: string
}

export interface Department {
  id: number
  name: string
  code: string
  parent_id: number | null
  sort: number
  status: number
  children?: Department[]
}

export interface Position {
  id: number
  name: string
  code: string
  sort: number
  status: number
}

export interface Menu {
  id: number
  name: string
  code: string
  type: number
  parent_id: number | null
  path?: string
  icon?: string
  sort: number
  status: number
  children?: Menu[]
}

export interface Role {
  id: number
  name: string
  code: string
  sort: number
  status: number
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface PageResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface LoginRequest {
  username: string
  password: string
  captcha_key: string
  captcha_code: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface CaptchaResponse {
  captcha_key: string
  captcha_image: string
}