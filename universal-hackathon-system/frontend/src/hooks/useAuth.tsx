import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api, setAuthToken } from '../services/api'

interface User { id: number; email: string; role: string }
interface AuthContextType {
  token: string | null
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType>(null as any)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    setAuthToken(token)
    if (token) {
      api.get('/auth/me').then(r => setUser(r.data)).catch(() => setUser(null))
    } else {
      setUser(null)
    }
  }, [token])

  const login = async (email: string, password: string) => {
    const r = await api.post('/auth/login', new URLSearchParams({ username: email, password }))
    const t = r.data.access_token
    setToken(t)
    localStorage.setItem('token', t)
  }

  const logout = () => {
    setToken(null)
    localStorage.removeItem('token')
  }

  const value = useMemo(() => ({ token, user, login, logout }), [token, user])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}