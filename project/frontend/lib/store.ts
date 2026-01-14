import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  token: string | null
  setToken: (token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      setToken: (token) => set({ token }),
      logout: () => set({ token: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
)

interface ResumeState {
  currentResumeId: string | null
  setCurrentResumeId: (id: string | null) => void
}

export const useResumeStore = create<ResumeState>()((set) => ({
  currentResumeId: null,
  setCurrentResumeId: (id) => set({ currentResumeId: id }),
}))
