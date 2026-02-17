"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, CheckCircle2, XCircle } from "lucide-react"
import { API_BASE } from "@/config/api"
import { useLanguage } from "@/contexts/LanguageContext"

const MAX_RETRIES = 2

export function OnboardingForm() {
  const { t } = useLanguage()
  const [step, setStep] = useState<"provider" | "validating" | "success" | "error">("provider")
  const [provider, setProvider] = useState("openai")
  const [apiKey, setApiKey] = useState("")
  const [models, setModels] = useState<string[]>([])
  const [selectedModel, setSelectedModel] = useState("")
  const [errorMsg, setErrorMsg] = useState("")
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

  // Cancel countdown when user modifies inputs
  useEffect(() => {
    if (isCountingDown && intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
      setIsCountingDown(false)
      setCountdown(0)
      setErrorMsg("")
    }
  }, [apiKey, provider, isCountingDown])

  // Fetch models when provider changes
  useEffect(() => {
    fetch(`${API_BASE}/models?provider=${provider}`)
      .then(res => res.json())
      .then(data => {
        setModels(data)
        if (data.length > 0) setSelectedModel(data[0])
      })
      .catch(err => console.error("Failed to fetch models", err))
  }, [provider])

  const getErrorMessage = (res: Response, err: { message?: string }) => {
    if (res.status === 404) {
      return t("error_backend_not_reachable")
    } else if (res.status === 401) {
      return t("error_invalid_api_key")
    } else if (res.status === 429) {
      return t("error_rate_limit")
    } else if (err.message) {
      return err.message
    } else {
      return t("error_validation_failed")
    }
  }

  const handleValidation = async () => {
    setStep("validating")
    setErrorMsg("")

    try {
      const res = await fetch(`${API_BASE}/settings/validate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider, api_key: apiKey }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        const message = getErrorMessage(res, { message: errorData.detail })
        throw new Error(message)
      }

      // If validation passes, save settings
      const saveRes = await fetch(`${API_BASE}/settings/save`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider,
          api_key: apiKey,
          model_preference: selectedModel
        }),
      })

      if (!saveRes.ok) throw new Error(t("error_save_failed"))

      setStep("success")

    } catch (err: unknown) {
      console.error(err)
      const errorMessage = err instanceof Error ? err.message : "An unknown error occurred"
      setErrorMsg(errorMessage)
      setStep("error")

      // Auto-retry logic with countdown
      // Only retry if we haven't exceeded max retries and not 404 (backend not reachable)
      if (retryCount < MAX_RETRIES && !errorMessage.includes("Backend server not reachable")) {
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
          handleValidation()
          setRetryCount(prevCount => prevCount + 1)
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
    setErrorMsg("")
    setStep("provider")
  }

  if (step === "success") {
    return (
      <div className="flex flex-col items-center justify-center space-y-4 p-8 border rounded-lg bg-green-50">
        <CheckCircle2 className="h-12 w-12 text-green-600" />
        <h2 className="text-xl font-bold text-green-800">{t("onboarding_success_title")}</h2>
        <p className="text-green-700">{t("onboarding_success_message")}</p>
        <Button onClick={() => window.location.reload()}>{t("onboarding_continue")}</Button>
      </div>
    )
  }

  return (
    <div className="max-w-md w-full mx-auto space-y-6 p-6 border rounded-xl shadow-sm bg-white">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold tracking-tight">{t("onboarding_welcome_title")}</h1>
        <p className="text-slate-500">{t("onboarding_welcome_description")}</p>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">{t("onboarding_provider_label")}</label>
          <select 
            className="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm"
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
          >
            <option value="openai">{t("onboarding_provider_openai")}</option>
            <option value="anthropic">{t("onboarding_provider_anthropic")}</option>
            <option value="ollama">{t("onboarding_provider_ollama")}</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">{t("onboarding_api_key_label")}</label>
          <Input 
            type="password" 
            placeholder={t("onboarding_api_key_placeholder")}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>

        {models.length > 0 && (
          <div className="space-y-2">
            <label className="text-sm font-medium">{t("onboarding_default_model_label")}</label>
            <select 
              className="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm"
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
            >
              {models.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
        )}

        {step === "error" && (
           <div className="p-4 text-sm bg-red-50 border border-red-200 rounded-md flex items-start gap-3 transition-opacity duration-300">
             <XCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
             <div className="flex-1 space-y-2">
               <p className="font-medium text-red-800">{errorMsg}</p>
               {countdown > 0 ? (
                 <p className="text-slate-600">
                   {t("onboarding_retrying_in", { countdown: countdown.toString() })}
                 </p>
               ) : retryCount >= MAX_RETRIES ? (
                 <p className="text-slate-600">
                   {t("onboarding_max_retries")}
                 </p>
               ) : null}
               {(countdown > 0 || retryCount >= MAX_RETRIES) && (
                 <Button
                   variant="outline"
                   size="sm"
                   onClick={handleCancelRetry}
                   className="mt-2 text-xs"
                 >
                   {t("onboarding_cancel_new_key")}
                 </Button>
               )}
             </div>
           </div>
         )}

        <Button 
          className="w-full" 
          onClick={handleValidation}
          disabled={step === "validating" || isCountingDown || !apiKey}
        >
          {step === "validating" ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              {t("onboarding_validating")}
            </>
          ) : isCountingDown ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              {t("onboarding_retrying_in", { countdown: countdown.toString() })}
            </>
          ) : (
            t("onboarding_validate_save")
          )}
        </Button>
      </div>
    </div>
  )
}
