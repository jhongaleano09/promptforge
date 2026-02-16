"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, CheckCircle2, XCircle } from "lucide-react"
import { API_BASE } from "@/config/api"

const MAX_RETRIES = 2

export function OnboardingForm() {
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
      return "Backend server not reachable. Please check your API configuration"
    } else if (res.status === 401) {
      return "Invalid API Key. Please check your credentials."
    } else if (res.status === 429) {
      return "Rate limit exceeded or insufficient quota. Please try again later."
    } else if (err.message) {
      return err.message
    } else {
      return "Validation failed. Please try again."
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

      if (!saveRes.ok) throw new Error("Failed to save settings")

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
        <h2 className="text-xl font-bold text-green-800">Setup Complete!</h2>
        <p className="text-green-700">Your API key has been securely stored.</p>
        <Button onClick={() => window.location.reload()}>Continue to App</Button>
      </div>
    )
  }

  return (
    <div className="max-w-md w-full mx-auto space-y-6 p-6 border rounded-xl shadow-sm bg-white">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold tracking-tight">Welcome to PromptForge</h1>
        <p className="text-slate-500">Configure your LLM provider to get started.</p>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Provider</label>
          <select 
            className="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm"
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
          >
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">API Key</label>
          <Input 
            type="password" 
            placeholder="sk-..." 
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>

        {models.length > 0 && (
          <div className="space-y-2">
            <label className="text-sm font-medium">Default Model</label>
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
                   Retrying in <span className="font-semibold">{countdown}s</span>...
                 </p>
               ) : retryCount >= MAX_RETRIES ? (
                 <p className="text-slate-600">
                   Maximum retry attempts reached. Please check your API key or try again.
                 </p>
               ) : null}
               {(countdown > 0 || retryCount >= MAX_RETRIES) && (
                 <Button
                   variant="outline"
                   size="sm"
                   onClick={handleCancelRetry}
                   className="mt-2 text-xs"
                 >
                   Cancel & Enter New Key
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
              Validating...
            </>
          ) : isCountingDown ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Retrying in {countdown}s...
            </>
          ) : (
            "Validate & Save"
          )}
        </Button>
      </div>
    </div>
  )
}
