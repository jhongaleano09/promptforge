'use client'

import { useState, useEffect } from 'react'
import { usePreferenceStore } from '@/store/preferenceStore'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Loader2, Save, CheckCircle2, Info } from 'lucide-react'
import { useLanguage } from '@/contexts/LanguageContext'

export function AdvancedSettings() {
  const { t } = useLanguage()
  const {
    defaultProvider,
    defaultModel,
    loading,
    error,
    loadPreferences,
    updatePreferences
  } = usePreferenceStore()

  const [localProvider, setLocalProvider] = useState(defaultProvider)
  const [localModel, setLocalModel] = useState(defaultModel)
  const [temperature, setTemperature] = useState(0.7)
  const [maxTokens, setMaxTokens] = useState(2000)
  const [topP, setTopP] = useState(1.0)
  const [saving, setSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)

  useEffect(() => {
    loadPreferences()
  }, [loadPreferences])

  useEffect(() => {
    setLocalProvider(defaultProvider)
    setLocalModel(defaultModel)
  }, [defaultProvider, defaultModel])

  const handleSave = async () => {
    setSaving(true)
    try {
      await updatePreferences({
        default_provider: localProvider,
        default_model: localModel
      })
      setLastSaved(new Date())
    } catch (err) {
      console.error('Failed to save advanced settings:', err)
    } finally {
      setSaving(false)
    }
  }

  const models: Record<string, string[]> = {
    openai: ['gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
    anthropic: ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'],
    ollama: ['llama3', 'mistral', 'gemma']
  }

  const availableModels = models[localProvider] || []

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{t("advanced_settings_title")}</CardTitle>
          <CardDescription>
            {t("advanced_settings_description")}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t("advanced_settings_default_provider")}</label>
              <select
                value={localProvider}
                onChange={(e) => setLocalProvider(e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                disabled={loading}
              >
                <option value="openai">{t("provider_selector_openai")}</option>
                <option value="anthropic">{t("provider_selector_anthropic")}</option>
                <option value="ollama">{t("provider_selector_ollama")}</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">{t("advanced_settings_default_model")}</label>
              <select
                value={localModel}
                onChange={(e) => setLocalModel(e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                disabled={loading}
              >
                {availableModels.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="space-y-4 pt-4 border-t">
            <div className="flex items-center gap-2 mb-2">
              <Info className="h-4 w-4 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                {t("advanced_settings_temperature_help")}
              </p>
            </div>

            <div className="space-y-3">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <label className="text-sm font-medium">{t("advanced_settings_temperature")}</label>
                  <span className="text-sm text-muted-foreground">{temperature.toFixed(2)}</span>
                </div>
                <Slider
                  value={[temperature]}
                  onValueChange={([value]) => setTemperature(value)}
                  min={0}
                  max={2}
                  step={0.1}
                  disabled={loading}
                />
                <p className="text-xs text-muted-foreground">
                  {t("advanced_settings_temperature_help")}
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <label className="text-sm font-medium">{t("advanced_settings_max_tokens")}</label>
                  <span className="text-sm text-muted-foreground">{maxTokens}</span>
                </div>
                <Slider
                  value={[maxTokens]}
                  onValueChange={([value]) => setMaxTokens(value)}
                  min={100}
                  max={4000}
                  step={100}
                  disabled={loading}
                />
                <p className="text-xs text-muted-foreground">
                  {t("advanced_settings_max_tokens_help")}
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <label className="text-sm font-medium">{t("advanced_settings_top_p")}</label>
                  <span className="text-sm text-muted-foreground">{topP.toFixed(2)}</span>
                </div>
                <Slider
                  value={[topP]}
                  onValueChange={([value]) => setTopP(value)}
                  min={0}
                  max={1}
                  step={0.1}
                  disabled={loading}
                />
                <p className="text-xs text-muted-foreground">
                  {t("advanced_settings_top_p_help")}
                </p>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t">
            <Button
              onClick={handleSave}
              disabled={saving || loading}
              size="sm"
            >
              {saving ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  {t("advanced_settings_saving")}
                </>
              ) : lastSaved ? (
                <>
                  <CheckCircle2 className="mr-2 h-4 w-4 text-green-600" />
                  {t("advanced_settings_saved")}
                </>
              ) : (
                <>
                  <Save className="mr-2 h-4 w-4" />
                  {t("advanced_settings_save_changes")}
                </>
              )}
            </Button>
          </div>

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
