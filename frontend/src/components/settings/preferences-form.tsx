'use client'

import { useState, useEffect } from 'react'
import { cn } from '@/lib/utils'
import { usePreferenceStore, Language } from '@/store/preferenceStore'
import { LanguageSwitcher } from '@/components/language-switcher'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Loader2, Save, CheckCircle2 } from 'lucide-react'
import { useLanguage } from '@/contexts/LanguageContext'

export function PreferencesForm() {
  const { t } = useLanguage()
  const {
    name,
    country,
    autoSave,
    theme,
    loading,
    error,
    loadPreferences,
    updatePreferences,
    setTheme
  } = usePreferenceStore()

  const [localName, setLocalName] = useState(name || '')
  const [localCountry, setLocalCountry] = useState(country || '')
  const [autoSaveEnabled, setAutoSaveEnabled] = useState(autoSave)
  const [saving, setSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)

  useEffect(() => {
    loadPreferences()
  }, [loadPreferences])

  useEffect(() => {
    setLocalName(name || '')
    setLocalCountry(country || '')
    setAutoSaveEnabled(autoSave)
  }, [name, country, autoSave])

  const handleSave = async () => {
    setSaving(true)
    try {
      await updatePreferences({
        name: localName || null,
        country: localCountry || null,
        autoSave: autoSaveEnabled
      })
      setLastSaved(new Date())
    } catch (err) {
      console.error('Failed to save preferences:', err)
    } finally {
      setSaving(false)
    }
  }

  const handleAutoSaveChange = (enabled: boolean) => {
    setAutoSaveEnabled(enabled)
    if (enabled) {
      updatePreferences({ autoSave: true })
      setLastSaved(new Date())
    }
  }

  const handleThemeToggle = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
    updatePreferences({ theme: newTheme })
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{t("preferences_form_title")}</CardTitle>
          <CardDescription>
            {t("preferences_form_description")}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t("preferences_form_your_name")}</label>
              <Input
                placeholder={t("preferences_form_name_placeholder")}
                value={localName}
                onChange={(e) => setLocalName(e.target.value)}
                onBlur={() => autoSaveEnabled && handleSave()}
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t("preferences_form_country")}</label>
              <Input
                placeholder={t("preferences_form_country_placeholder")}
                value={localCountry}
                onChange={(e) => setLocalCountry(e.target.value)}
                onBlur={() => autoSaveEnabled && handleSave()}
                disabled={loading}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">{t("preferences_form_language")}</label>
            <LanguageSwitcher />
          </div>

          <div className="flex items-center justify-between py-2 border-t">
            <div className="space-y-0.5">
              <label className="text-sm font-medium">{t("preferences_form_auto_save")}</label>
              <p className="text-xs text-muted-foreground">
                {t("preferences_form_auto_save_help")}
              </p>
            </div>
            <button
              onClick={() => handleAutoSaveChange(!autoSaveEnabled)}
              className={cn(
                "relative inline-flex h-6 w-11 items-center rounded-full transition-colors",
                autoSaveEnabled ? "bg-primary" : "bg-input"
              )}
              type="button"
            >
              <span
                className={cn(
                  "inline-block h-4 w-4 transform rounded-full bg-white transition-transform",
                  autoSaveEnabled ? "translate-x-6" : "translate-x-1"
                )}
              />
            </button>
          </div>

          <div className="flex items-center justify-between py-2 border-t">
            <div className="space-y-0.5">
              <label className="text-sm font-medium">{t("preferences_form_theme")}</label>
              <p className="text-xs text-muted-foreground">
                {theme === 'light' ? t("preferences_form_light_mode") : t("preferences_form_dark_mode")}
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleThemeToggle}
              disabled={loading}
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </Button>
          </div>

          {!autoSaveEnabled && (
            <div className="flex items-center justify-between py-2 border-t">
              <div className="space-y-0.5">
                <label className="text-sm font-medium">{t("preferences_form_save_changes")}</label>
                {lastSaved && (
                  <p className="text-xs text-muted-foreground">
                    {t("preferences_form_last_saved")} {lastSaved.toLocaleTimeString()}
                  </p>
                )}
              </div>
              <Button
                onClick={handleSave}
                disabled={saving || loading}
                size="sm"
              >
                {saving ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {t("preferences_form_saving")}
                  </>
                ) : lastSaved ? (
                  <>
                    <CheckCircle2 className="mr-2 h-4 w-4 text-green-600" />
                    {t("preferences_form_saved")}
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    {t("preferences_form_save")}
                  </>
                )}
              </Button>
            </div>
          )}

          {error && (
            <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-md">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
