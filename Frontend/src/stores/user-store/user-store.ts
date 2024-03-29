import router from '@/router'
import { defineStore } from 'pinia'
import type { Assistant } from './models/Assistant'
import type { Histories } from './models/Histories'
import type { User } from './models/User'
import { UserService } from './service/user.service'

interface State {
  user: User
  isLoading: boolean
  assistants: Assistant[]
  histories: Histories[]
  isHistories: boolean
  selectedAssistant: number
}

export const useUserStore = defineStore('useUserStore', {
  state: (): State => ({
    user: { id: 0, pseudo: '' },
    isLoading: false,
    assistants: [],
    histories: [],
    isHistories: true,
    selectedAssistant: -1
  }),
  getters: {
    getUser: (state) => state.user,
    getIsLoading: (state) => state.isLoading,
    getAssistants: (state) => state.assistants,
    getHistory: (state) => state.histories,
    getIsHistories: (state) => state.isHistories,
    getSelectedAssistant: (state) => state.selectedAssistant
  },
  actions: {
    async register(pseudo: string, password: string): Promise<boolean> {
      this.isLoading = true
      const user = await UserService.register(pseudo, password)
      this.user = user
      this.isLoading = false
      if (user) {
        router.push('/dashboard')
        this.fetchAssistants()
        return true
      } else {
        return false
      }
    },

    async login(pseudo: string, password: string): Promise<boolean> {
      this.isLoading = true
      const user = await UserService.login(pseudo, password)
      this.user = user
      this.isLoading = false
      if (user) {
        router.push('/dashboard')
        this.fetchAssistants()
        return true
      } else {
        return false
      }
    },

    async fetchAssistants() {
      this.isLoading = true
      this.isHistories = true
      this.selectedAssistant = -1
      this.histories = []
      const assistants = await UserService.getAssistants(this.user.id)
      this.assistants = assistants
      this.isLoading = false
    },

    setHistory(index: number) {
      this.histories = this.assistants[index].histories
      this.isHistories = true
      this.selectedAssistant = index
    },

    setSettings(index: number) {
      this.isHistories = false
      this.selectedAssistant = index
    },

    async addAssistant(id: number, code: number) {
      this.isLoading = true
      const response = await UserService.addAssistant(id, code)
      if (response) {
        this.fetchAssistants()
      }
      this.isLoading = false
      return response
    },

    async setAssistantConfiguration(
      language: string,
      voice: string,
      wifiSSID: string,
      wifiPassword: string
    ) {
      this.isLoading = true
      await UserService.setAssistantConfiguration(
        this.getAssistants[this.getSelectedAssistant].code,
        language,
        voice,
        wifiSSID,
        wifiPassword
      )
      this.fetchAssistants()
      this.isLoading = false
    }
  }
})
