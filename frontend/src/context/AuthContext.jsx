import { createContext, useContext, useState } from 'react'
import api from '../api/axios'

// Context is a way to share state across all components
// without passing props down through every level.
// Any component can call useAuth() to get the user and login/logout functions.
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  // Initialize user from localStorage so login persists on page refresh
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user')
    return saved ? JSON.parse(saved) : null
  })

  const login = async (email, password) => {
    // POST to Django's login endpoint — returns access + refresh tokens
    const res = await api.post('/auth/login/', { email, password })
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)

    // Fetch the user profile and store it
    const userRes = await api.get('/auth/me/')
    localStorage.setItem('user', JSON.stringify(userRes.data))
    setUser(userRes.data)
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout/', { refresh: localStorage.getItem('refresh_token') })
    } catch {
      // even if blacklist fails, clear local state
    }
    localStorage.clear()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook — components call useAuth() instead of useContext(AuthContext)
export function useAuth() {
  return useContext(AuthContext)
}
