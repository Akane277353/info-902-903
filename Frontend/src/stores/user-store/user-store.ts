import router from '@/router'
import { defineStore } from 'pinia'
import type { Assistant } from './models/Assistant'
import type { User } from './models/User'
import { UserService } from './service/user.service'

interface State {
  user: User | null
  isLoading: boolean
  assistants: Assistant[]
}

export const useUserStore = defineStore('useUserStore', {
  state: (): State => ({
    user: null,
    isLoading: false,
    assistants: []
  }),
  getters: {
    getUser: (state) => state.user,
    getIsLoading: (state) => state.isLoading,
    getAssistants: (state) => state.assistants
  },
  actions: {
    async register(pseudo: string, password: string) {
      this.isLoading = true
      const user = await UserService.register(pseudo, password)
      this.user = user
      this.isLoading = false
      if (user) {
        router.push('/dashboard')
        this.fetchAssistants(user.id)
      }
    },

    async login(pseudo: string, password: string) {
      this.isLoading = true
      const user = await UserService.login(pseudo, password)
      this.user = user
      this.isLoading = false
      if (user) {
        router.push('/dashboard')
        this.fetchAssistants(user.id)
      }
    },

    async fetchAssistants(userId: number) {
      this.isLoading = true
      const assistants = await UserService.getAssistants(userId)
      this.assistants = assistants
      this.isLoading = false
    }
  }
})
