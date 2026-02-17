'use client';

/**
 * Language Context
 * 
 * Provides language preference and translation functions throughout the app.
 * Single-user application: language preference is stored in database.
 */

import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { interpolate } from '@/lib/i18n-utils';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Types
export type Language = 'spanish' | 'english';

export interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => Promise<void>;
  t: (key: string, vars?: Record<string, string | number>) => string;
  isLoading: boolean;
}

// Create Context
const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Provider Component
export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>('spanish');
  const [translations, setTranslations] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Load translations from JSON file
   */
  const loadTranslations = useCallback(async (lang: Language) => {
    setIsLoading(true);
    try {
      const res = await fetch(`/i18n/${lang}.json`);
      if (!res.ok) {
        throw new Error(`Failed to load translations: ${res.status}`);
      }
      const data = await res.json();
      setTranslations(data);
    } catch (error) {
      console.error('Error loading translations:', error);
      // Fallback to empty translations
      setTranslations({});
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Load language preference from backend
   */
  const loadSavedLanguage = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/user/preferences/language`);
      if (res.ok) {
        const data = await res.json();
        const savedLang = data.language as Language;
        setLanguageState(savedLang);
        await loadTranslations(savedLang);
      } else {
        // If fails, use default
        await loadTranslations('spanish');
      }
    } catch (error) {
      console.error('Error loading saved language:', error);
      await loadTranslations('spanish');
    }
  }, [loadTranslations]);

  /**
   * Change language preference
   */
  const setLanguage = useCallback(async (lang: Language) => {
    try {
      // Update local state immediately for responsive UI
      setLanguageState(lang);
      
      // Load new translations
      await loadTranslations(lang);
      
      // Save to localStorage as cache
      localStorage.setItem('promptforge_language', lang);
      
      // Save to backend
      await fetch(`${API_BASE}/user/preferences/language`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: lang }),
      });
    } catch (error) {
      console.error('Error updating language preference:', error);
    }
  }, [loadTranslations]);

  /**
   * Translation function with interpolation support
   */
  const t = useCallback((key: string, vars?: Record<string, string | number>): string => {
    const translation = translations[key];
    
    if (!translation) {
      // Return the key itself if translation not found (useful for development)
      console.warn(`Translation missing for key: "${key}"`);
      return key;
    }
    
    // Apply interpolation if vars provided
    return interpolate(translation, vars);
  }, [translations]);

  /**
   * Initialize language on mount
   */
  useEffect(() => {
    const initLanguage = async () => {
      // Try localStorage first (for faster initial render)
      const cachedLang = localStorage.getItem('promptforge_language') as Language | null;
      
      if (cachedLang && (cachedLang === 'spanish' || cachedLang === 'english')) {
        setLanguageState(cachedLang);
        await loadTranslations(cachedLang);
      }
      
      // Then load from backend (authoritative source)
      await loadSavedLanguage();
    };
    
    initLanguage();
  }, [loadSavedLanguage, loadTranslations]);

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t, isLoading }}>
      {children}
    </LanguageContext.Provider>
  );
}

/**
 * Custom hook to access language context
 */
export function useLanguage(): LanguageContextType {
  const context = useContext(LanguageContext);
  
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  
  return context;
}
