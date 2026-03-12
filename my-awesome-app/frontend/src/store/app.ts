import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const activeTab = ref<string>('/dashboard')
  const tabs = ref<Array<{ path: string; title: string; name: string }>>([])

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const addTab = (tab: { path: string; title: string; name: string }) => {
    const exists = tabs.value.find((t) => t.path === tab.path)
    if (!exists) {
      tabs.value.push(tab)
    }
    activeTab.value = tab.path
  }

  const removeTab = (path: string) => {
    const index = tabs.value.findIndex((t) => t.path === path)
    if (index > -1) {
      tabs.value.splice(index, 1)
      if (activeTab.value === path && tabs.value.length > 0) {
        activeTab.value = tabs.value[tabs.value.length - 1].path
      }
    }
  }

  const clearTabs = () => {
    tabs.value = []
    activeTab.value = '/dashboard'
  }

  return {
    sidebarCollapsed,
    activeTab,
    tabs,
    toggleSidebar,
    addTab,
    removeTab,
    clearTabs,
  }
})