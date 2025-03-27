import apiClient, { endpoints } from './api'
import emitter from '../utils/eventBus'

// Authentication service
const authService = {
  // Login method
  async login(credentials) {
    try {
      const response = await apiClient.post(endpoints.auth.login, credentials)
      const token = response.data.token
      localStorage.setItem(import.meta.env.VITE_AUTH_TOKEN_NAME || 'authToken', token)
      emitter.emit('auth-change', { status: 'login' })
      return response.data
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  },
  
  // Logout method
  logout() {
    localStorage.removeItem(import.meta.env.VITE_AUTH_TOKEN_NAME || 'authToken')
    emitter.emit('auth-change', { status: 'logout' })
  },
  
  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem(import.meta.env.VITE_AUTH_TOKEN_NAME || 'authToken')
  },
  
  // Get current user information
  async getCurrentUser() {
    try {
      const response = await apiClient.get(endpoints.user.profile)
      return response.data
    } catch (error) {
      console.error('Error fetching user data:', error)
      throw error
    }
  }
}

export default authService
