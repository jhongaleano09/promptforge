"use client"

import { useLanguage } from "@/contexts/LanguageContext"
import { cn } from "@/lib/utils"

export function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage()

  return (
    <div className="flex items-center gap-1 bg-muted/50 p-1 rounded-lg border">
      <button
        onClick={() => setLanguage('spanish')}
        className={cn(
          "px-3 py-1.5 rounded-md text-sm font-medium transition-all flex items-center gap-1.5",
          language === 'spanish' 
            ? "bg-background shadow-sm text-foreground ring-1 ring-border" 
            : "text-muted-foreground hover:text-foreground"
        )}
      >
        <span className="text-base">🇪🇸</span>
        <span>Español</span>
      </button>
      <button
        onClick={() => setLanguage('english')}
        className={cn(
          "px-3 py-1.5 rounded-md text-sm font-medium transition-all flex items-center gap-1.5",
          language === 'english' 
            ? "bg-background shadow-sm text-foreground ring-1 ring-border" 
            : "text-muted-foreground hover:text-foreground"
        )}
      >
        <span className="text-base">🇬🇧</span>
        <span>English</span>
      </button>
    </div>
  )
}
