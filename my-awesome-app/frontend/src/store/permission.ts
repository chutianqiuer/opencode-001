import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePermissionStore = defineStore('permission', () => {
  const routes = ref<unknown[]>([])
  const permissions = ref<string[]>([])

  const setRoutes = (newRoutes: unknown[]) => {
    routes.value = newRoutes
  }

  const setPermissions = (newPermissions: string[]) => {
    permissions.value = newPermissions
  }

  const clearRoutes = () => {
    routes.value = []
  }

  const clearPermissions = () => {
    permissions.value = []
  }

  const hasPermission = (permission: string): boolean => {
    return permissions.value.includes(permission)
  }

  const hasPermissions = (perms: string[], requireAll = false): boolean => {
    if (requireAll) {
      return perms.every((p) => permissions.value.includes(p))
    }
    return perms.some((p) => permissions.value.includes(p))
  }

  return {
    routes,
    permissions,
    setRoutes,
    setPermissions,
    clearRoutes,
    clearPermissions,
    hasPermission,
    hasPermissions,
  }
})