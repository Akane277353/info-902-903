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

  static async addAssistant(id: number, code: number): Promise<boolean> {
    const params = {
      idUser: id,
      code: code
    }
    try {
      const response = await instance.post<boolean>('/user/associate', params)
      return response.data
    } catch (e) {
      return Promise.reject(e)
    }
  }

  static async setAssistantConfiguration(
    code: number,
    language: string,
    voice: string,
    wifiSSID: string,
    wifiPassword: string
  ) {
    const params = {
      code: code,
      language: language,
      voice: voice,
      wifiSSID: wifiSSID,
      wifiPassword: wifiPassword
    }
    try {
      await instance.post<void>('/assistant/setconfig', params)
    } catch (e) {
      return Promise.reject(e)
    }
  }
}
