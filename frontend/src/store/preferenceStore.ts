import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { API_BASE } from '@/config/api'

export type Language = 'spanish' | 'english'
export type Theme = 'light' | 'dark'

export interface Preferences {
  language: Language
  name: string | null
  country: string | null
  defaultProvider: string
  defaultModel: string
  autoSave: boolean
  theme: Theme
}

export interface PreferenceStore extends Preferences {
  loading: boolean
  error: string | null
  loadPreferences: () => Promise<void>
  updatePreferences: (prefs: Partial<Preferences>) => Promise<void>
  setLanguage: (lang: Language) => Promise<void>
  setTheme: (theme: Theme) => void
}

export const usePreferenceStore = create<PreferenceStore>()(
  persist(
    (set, get) => ({
      // Default values
      language: 'spanish',
      name: null,
      country: null,
      defaultProvider: 'openai',
      defaultModel: 'gpt-4-turbo',
      autoSave: true,
      theme: 'light',
      loading: false,
      error: null,

      loadPreferences: async () => {
        set({ loading: true, error: null })
        try {
          const res = await fetch(`${API_BASE}/user/preferences`)
          if (!res.ok) {
            throw new Error('Failed to load preferences')
          }
          const data = await res.json()
          set({
            ...data,
            loading: false
          })
        } catch (e: any) {
          set({ error: e.message, loading: false })
          console.error('Error loading preferences:', e)
        }
      },

      updatePreferences: async (prefs) => {
        const current = get()
        const updated: Preferences = {
          language: prefs.language ?? current.language,
          name: prefs.name !== undefined ? prefs.name : current.name,
          country: prefs.country !== undefined ? prefs.country : current.country,
          defaultProvider: prefs.defaultProvider ?? current.defaultProvider,
          defaultModel: prefs.defaultModel ?? current.defaultModel,
          autoSave: prefs.autoSave !== undefined ? prefs.autoSave : current.autoSave,
          theme: prefs.theme ?? current.theme
        }

        set({ loading: true, error: null })

        try {
          const res = await fetch(`${API_BASE}/user/preferences`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(prefs)
          })

          if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || 'Failed to update preferences')
          }

          set(updated)
        } catch (e: any) {
          set({ error: e.message, loading: false })
          console.error('Error updating preferences:', e)
          throw e
        } finally {
          set({ loading: false })
        }
      },

      setLanguage: async (lang) => {
        await get().updatePreferences({ language: lang })
      },

      setTheme: (theme) => {
        set({ theme })
        document.documentElement.classList.toggle('dark', theme === 'dark')
      }
    }),
    {
      name: 'promptforge-preferences',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        language: state.language,
        theme: state.theme
      })
    }
  )
)
