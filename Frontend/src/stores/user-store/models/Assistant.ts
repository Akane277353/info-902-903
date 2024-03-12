import type { Histories } from './Histories'

export interface Assistant {
  code: number
  language: string
  voice: string
  wifiSSID: string
  wifiPassword: string
  histories: Histories[]
}
