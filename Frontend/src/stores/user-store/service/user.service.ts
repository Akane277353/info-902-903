import instance from '@/axios/axios'
import type { Assistant } from '../models/Assistant'
import type { User } from '../models/User'

export class UserService {
  static async register(pseudo: string, password: string): Promise<User> {
    const params = {
      pseudo: pseudo,
      password: password
    }
    try {
      const response = await instance.post<User>('/user/register', params)
      return response.data
    } catch (e) {
      return Promise.reject(e)
    }
  }

  static async login(pseudo: string, password: string): Promise<User> {
    const params = {
      pseudo: pseudo,
      password: password
    }
    try {
      const response = await instance.post<User>('/user/login', params)
      return response.data
    } catch (e) {
      return Promise.reject(e)
    }
  }

  static async getAssistants(userId: number): Promise<Assistant[]> {
    try {
      const response = await instance.get<Assistant[]>(`assistant/assistantsofuser/` + userId)
      return response.data
    } catch (e) {
      return Promise.reject(e)
    }
  }
}
