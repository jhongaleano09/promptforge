"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Loader2, CheckCircle2, XCircle, Settings, Key, Trash2, Plus, RefreshCw, AlertTriangle } from "lucide-react"
import { API_BASE } from "@/config/api"
import { useLanguage } from "@/contexts/LanguageContext"

interface ApiKey {
  id: number
  provider: string
  model_preference: string
  is_active: boolean
  usage_count: number
  created_at: string
  updated_at?: string
}

interface ValidationActiveResponse {
  has_active_key: boolean
  active_providers: string[]
  all_providers: string[]
  warning?: string
}

const MAX_RETRIES = 2

export function ApiKeysManager() {
  const { t } = useLanguage()
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [keyToDelete, setKeyToDelete] = useState<ApiKey | null>(null)
  const [showAllKeys, setShowAllKeys] = useState(false)
  const [validationStatus, setValidationStatus] = useState<ValidationActiveResponse | null>(null)

  // Add Modal States
  const [provider, setProvider] = useState("openai")
  const [apiKey, setApiKey] = useState("")
  const [modelPreference, setModelPreference] = useState("")
  const [models, setModels] = useState<string[]>([])
  const [validating, setValidating] = useState(false)
  const [addError, setAddError] = useState<string | null>(null)
  const [isValidatingKey, setIsValidatingKey] = useState(false)

  // Delete Modal States
  const [deleting, setDeleting] = useState(false)
  const [retryCount, setRetryCount] = useState(0)
  const [countdown, setCountdown] = useState(0)
  const [isCountingDown, setIsCountingDown] = useState(false)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  // Cleanup interval on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [])

  // Fetch models when provider changes
  useEffect(() => {
    fetch(`${API_BASE}/models?provider=${provider}`)
      .then(res => res.json())
      .then(data => {
        setModels(data)
        if (data.length > 0) setModelPreference(data[0])
      })
      .catch(err => console.error("Failed to fetch models", err))
  }, [provider])

  // Load API keys and validation status
  useEffect(() => {
    loadApiKeys()
    validateConfiguration()
  }, [])

  // Cancel countdown when user modifies inputs
  useEffect(() => {
    if (isCountingDown && intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
      setIsCountingDown(false)
      setCountdown(0)
      setAddError("")
    }
  }, [apiKey, provider, isCountingDown])

  const loadApiKeys = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/settings/keys`)
      const data = await res.json()
      setApiKeys(data.keys || [])
    } catch (err: any) {
      setError(err.message || t("errors_failed_load_api_keys"))
    } finally {
      setLoading(false)
    }
  }

  const validateConfiguration = async () => {
    try {
      const res = await fetch(`${API_BASE}/settings/validate-active`)
      const data = await res.json()
      setValidationStatus(data)
    } catch (err) {
      console.error(t("errors_failed_validate"), err)
    }
  }

  const validateApiKeyFormat = (key: string) => {
    if (!key || key.length < 10) return false

    if (provider === "openai") {
      return key.startsWith("sk-")
    } else if (provider === "anthropic") {
      return key.startsWith("sk-ant-")
    } else if (provider === "ollama") {
      return true // Ollama keys are not standardized
    }
    return false
  }

  const handleAddKey = async () => {
    if (!apiKey || !modelPreference) {
      setAddError(t("errors_fill_all_fields"))
      return
    }

    if (!validateApiKeyFormat(apiKey)) {
      setAddError(t("errors_invalid_api_key_format", { provider }))
      return
    }

    setValidating(true)
    setAddError(null)

    try {
      const res = await fetch(`${API_BASE}/settings/keys`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider,
          api_key: apiKey,
          model_preference: modelPreference
        }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || t("api_keys_error_add"))
      }

      await loadApiKeys()
      await validateConfiguration()
      setShowAddModal(false)
      setApiKey("")
      setProvider("openai")
      setModelPreference("")
    } catch (err: unknown) {
      console.error(err)
      const errorMessage = err instanceof Error ? err.message : t("errors_unknown_error")
      setAddError(errorMessage)
      setValidating(false)

      if (retryCount < MAX_RETRIES && !errorMessage.includes(t("errors_backend_not_reachable"))) {
        startRetryCountdown()
      } else {
        setRetryCount(MAX_RETRIES)
      }
    }
  }

  const startRetryCountdown = () => {
    setIsCountingDown(true)
    setCountdown(10)

    if (intervalRef.current) {
      clearInterval(intervalRef.current)
    }

    intervalRef.current = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          if (intervalRef.current) {
            clearInterval(intervalRef.current)
            intervalRef.current = null
          }
          setIsCountingDown(false)
          handleAddKey()
          setRetryCount((prevCount) => prevCount + 1)
          return 0
        }
        return prev - 1
      })
    }, 1000)
  }

  const handleCancelRetry = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
    setIsCountingDown(false)
    setCountdown(0)
    setRetryCount(0)
    setAddError("")
    setValidating(false)
  }

  const handleDeleteKey = async () => {
    if (!keyToDelete) return

    setDeleting(true)
    try {
      const res = await fetch(`${API_BASE}/settings/keys/${keyToDelete.id}`, {
        method: "DELETE",
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || t("api_keys_error_delete"))
      }

      await loadApiKeys()
      await validateConfiguration()
      setShowDeleteModal(false)
      setKeyToDelete(null)
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : t("errors_unknown_error")
      setAddError(errorMessage)

      if (retryCount < MAX_RETRIES && !errorMessage.includes(t("errors_backend_not_reachable"))) {
        startRetryCountdown()
      } else {
        setRetryCount(MAX_RETRIES)
      }
    } finally {
      setDeleting(false)
    }
  }

  const handleActivateKey = async (keyId: number) => {
    try {
      const res = await fetch(`${API_BASE}/settings/keys/${keyId}/activate`, {
        method: "PUT",
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || t("api_keys_error_activate"))
      }

      await loadApiKeys()
      await validateConfiguration()
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t("api_keys_error_activate"))
    }
  }

  const showDeleteConfirmation = (key: ApiKey) => {
    setKeyToDelete(key)
    setShowDeleteModal(true)
  }

  const activeKey = apiKeys.find(k => k.is_active)
  const inactiveKeys = apiKeys.filter(k => !k.is_active)
  const displayedKeys = showAllKeys ? apiKeys : (activeKey ? [activeKey] : [])

  const getProviderIcon = (provider: string) => {
    return <Key className="w-5 h-5" />
  }

  const getProviderColor = (provider: string) => {
    switch (provider) {
      case "openai":
        return "bg-blue-100 text-blue-800 border-blue-300"
      case "anthropic":
        return "bg-purple-100 text-purple-800 border-purple-300"
      case "ollama":
        return "bg-green-100 text-green-800 border-green-300"
      default:
        return "bg-gray-100 text-gray-800 border-gray-300"
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">{t("api_keys_title")}</h2>
          <p className="text-muted-foreground">{t("api_keys_description")}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={loadApiKeys} disabled={loading}>
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
          </Button>
          <Button onClick={() => setShowAddModal(true)}>
            <Plus className="w-4 h-4 mr-2" />
            {t("api_keys_add_new")}
          </Button>
        </div>
      </div>

      {/* Validation Warning */}
      {validationStatus?.warning && (
        <Card className="border-orange-200 bg-orange-50">
          <CardContent className="pt-6">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="font-medium text-orange-800">{t("api_keys_validation_required")}</p>
                <p className="text-sm text-orange-700">{validationStatus.warning}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* API Keys List */}
      {displayedKeys.length === 0 ? (
        <Card>
          <CardContent className="pt-6 text-center">
            <Settings className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">{t("api_keys_no_keys")}</p>
            <Button onClick={() => setShowAddModal(true)} className="mt-4">
              <Plus className="w-4 h-4 mr-2" />
              {t("api_keys_add_first")}
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {displayedKeys.map((key) => (
            <Card key={key.id} className={key.is_active ? "border-primary border-2" : ""}>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className={`p-3 rounded-lg border ${getProviderColor(key.provider)}`}>
                      {getProviderIcon(key.provider)}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold capitalize">{key.provider}</h3>
                        {key.is_active && (
                          <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">{t("api_keys_active")}</span>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {t("api_keys_model")}: {key.model_preference} · {t("api_keys_usage")}: {key.usage_count} {t("api_keys_tokens")}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {t("api_keys_created")}: {new Date(key.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {!key.is_active && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleActivateKey(key.id)}
                      >
                        {t("api_keys_activate")}
                      </Button>
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => showDeleteConfirmation(key)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}

          {/* Show All Keys Toggle */}
          {!showAllKeys && inactiveKeys.length > 0 && (
            <Button
              variant="ghost"
              onClick={() => setShowAllKeys(true)}
              className="w-full"
            >
              {t("api_keys_show_all", { count: inactiveKeys.length })}
            </Button>
          )}

          {showAllKeys && (
            <Button
              variant="ghost"
              onClick={() => setShowAllKeys(false)}
              className="w-full"
            >
              {t("api_keys_show_active_only")}
            </Button>
          )}
        </div>
      )}

      {/* Add Key Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>{t("api_keys_modal_add_title")}</CardTitle>
              <CardDescription>{t("api_keys_modal_add_description")}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">{t("api_keys_modal_provider_label")}</label>
                <select
                  className="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm"
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                >
                  <option value="openai">{t("api_keys_modal_provider_openai")}</option>
                  <option value="anthropic">{t("api_keys_modal_provider_anthropic")}</option>
                  <option value="ollama">{t("api_keys_modal_provider_ollama")}</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">{t("api_keys_modal_api_key_label")}</label>
                <div className="relative">
                  <Input
                    type="password"
                    placeholder={t("api_keys_modal_api_key_placeholder")}
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    disabled={validating || isCountingDown}
                  />
                  {apiKey && validateApiKeyFormat(apiKey) && (
                    <CheckCircle2 className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-green-600" />
                  )}
                  {apiKey && !validateApiKeyFormat(apiKey) && (
                    <XCircle className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-red-600" />
                  )}
                </div>
              </div>

              {models.length > 0 && (
                <div className="space-y-2">
                  <label className="text-sm font-medium">{t("api_keys_modal_default_model_label")}</label>
                  <select
                    className="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm"
                    value={modelPreference}
                    onChange={(e) => setModelPreference(e.target.value)}
                    disabled={validating || isCountingDown}
                  >
                    {models.map((m) => (
                      <option key={m} value={m}>
                        {m}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {addError && (
                <div className="p-4 text-sm bg-red-50 border border-red-200 rounded-md flex items-start gap-3">
                  <XCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <div className="flex-1 space-y-2">
                    <p className="font-medium text-red-800">{addError}</p>
                    {countdown > 0 ? (
                      <p className="text-slate-600">
                        {t("validation_retrying_in", { countdown: countdown })}
                      </p>
                    ) : retryCount >= MAX_RETRIES ? (
                      <p className="text-slate-600">
                        {t("validation_max_retries")}
                      </p>
                    ) : null}
                    {(countdown > 0 || retryCount >= MAX_RETRIES) && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleCancelRetry}
                        className="mt-2 text-xs"
                      >
                        {t("validation_cancel")}
                      </Button>
                    )}
                  </div>
                </div>
              )}

              <div className="flex gap-2 pt-2">
                <Button
                  variant="outline"
                  onClick={() => {
                    setShowAddModal(false)
                    setApiKey("")
                    setAddError(null)
                    setRetryCount(0)
                    setIsCountingDown(false)
                    setCountdown(0)
                  }}
                  disabled={validating || isCountingDown}
                  className="flex-1"
                >
                  {t("api_keys_modal_cancel")}
                </Button>
                <Button
                  onClick={handleAddKey}
                  disabled={validating || isCountingDown || !apiKey || !modelPreference}
                  className="flex-1"
                >
                  {validating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t("api_keys_modal_validating")}
                    </>
                  ) : isCountingDown ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t("validation_retrying_in", { countdown: countdown })}
                    </>
                  ) : (
                    t("api_keys_modal_add_button")
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && keyToDelete && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>{t("api_keys_modal_delete_title")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-sm text-muted-foreground">
                {t("api_keys_modal_delete_description", { provider: keyToDelete.provider })}
              </div>
              {keyToDelete.is_active && activeKey && apiKeys.length === 1 && (
                <div className="p-4 bg-orange-50 border border-orange-200 rounded-md">
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium text-orange-800">{t("api_keys_modal_delete_warning")}</p>
                      <p className="text-sm text-orange-700">
                        {t("api_keys_modal_delete_warning_message")}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {addError && (
                <div className="p-4 text-sm bg-red-50 border border-red-200 rounded-md flex items-start gap-3">
                  <XCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <div className="flex-1 space-y-2">
                    <p className="font-medium text-red-800">{addError}</p>
                    {countdown > 0 ? (
                      <p className="text-slate-600">
                        {t("validation_retrying_in", { countdown: countdown })}
                      </p>
                    ) : retryCount >= MAX_RETRIES ? (
                      <p className="text-slate-600">
                        {t("validation_max_retries")}
                      </p>
                    ) : null}
                    {(countdown > 0 || retryCount >= MAX_RETRIES) && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleCancelRetry}
                        className="mt-2 text-xs"
                      >
                        {t("validation_cancel")}
                      </Button>
                    )}
                  </div>
                </div>
              )}

              <div className="flex gap-2 pt-2">
                <Button
                  variant="outline"
                  onClick={() => {
                    setShowDeleteModal(false)
                    setKeyToDelete(null)
                    setAddError(null)
                    setRetryCount(0)
                    setIsCountingDown(false)
                    setCountdown(0)
                  }}
                  disabled={deleting || isCountingDown}
                  className="flex-1"
                >
                  {t("api_keys_modal_cancel")}
                </Button>
                <Button
                  variant="destructive"
                  onClick={handleDeleteKey}
                  disabled={deleting || isCountingDown}
                  className="flex-1"
                >
                  {deleting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t("api_keys_modal_deleting")}
                    </>
                  ) : isCountingDown ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t("validation_retrying_in", { countdown: countdown })}
                    </>
                  ) : (
                    t("api_keys_modal_delete_button")
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
