import { defineStore } from 'pinia'
import { authApi } from '../api'

export const useAppStore = defineStore('app', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
  }),
  actions: {
    async login(phone, password) {
      const { data } = await authApi.login(phone, password)
      if (data.success && data.user) {
        this.user = data.user
        this.token = 'demo-token'
        localStorage.setItem('token', this.token)
        return true
      }
      return false
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    },
    async fetchUser() {
      if (!this.token) return
      const { data } = await authApi.getUser()
      this.user = data
    },
  },
})
