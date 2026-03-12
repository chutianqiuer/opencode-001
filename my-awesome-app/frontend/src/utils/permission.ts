import { useUserStore } from '@/store/user'

export function hasPermission(permission: string): boolean {
  const userStore = useUserStore()
  const permissions = (userStore.userInfo as { permissions?: string[] }).permissions || []
  return permissions.includes(permission)
}

export function hasPermissions(permissions: string[], requireAll = false): boolean {
  if (requireAll) {
    return permissions.every((p) => hasPermission(p))
  }
  return permissions.some((p) => hasPermission(p))
}

export function checkPermission(el: HTMLElement, binding: { value: string | string[] }) {
  const value = binding.value
  if (!value) return

  const permissions = Array.isArray(value) ? value : [value]
  const hasAuth = hasPermissions(permissions)

  if (!hasAuth) {
    el.parentNode?.removeChild(el)
  }
}

export const permissionDirective = {
  mounted(el: HTMLElement, binding: { value: string | string[] }) {
    checkPermission(el, binding)
  },
}