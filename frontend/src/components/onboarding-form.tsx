"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, AlertCircle, CheckCircle2 } from "lucide-react"

export function OnboardingForm() {
  const [step, setStep] = useState<"provider" | "validating" | "success" | "error">("provider")
  const [provider, setProvider] = useState("openai")
  const [apiKey, setApiKey] = useState("")
  const [models, setModels] = useState<string[]>([])
  const [selectedModel, setSelectedModel] = useState("")
  const [errorMsg, setErrorMsg] = useState("")
  const [retryCount, setRetryCount] = useState(0)
  const [countdown, setCountdown] = useState(0)

  // Fetch models when provider changes
  useEffect(() => {
    fetch(`http://localhost:8001/api/models?provider=${provider}`)
      .then(res => res.json())
      .then(data => {
        setModels(data)
        if (data.length > 0) setSelectedModel(data[0])
      })
      .catch(err => console.error("Failed to fetch models", err))
  }, [provider])

  const handleValidation = async () => {
    setStep("validating")
    setErrorMsg("")
    
    try {
      const res = await fetch("http://localhost:8001/api/settings/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider, api_key: apiKey }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || "Validation failed")
      }

      // If validation passes, save settings
      const saveRes = await fetch("http://localhost:8001/api/settings/save", {
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

    } catch (err: any) {
      console.error(err)
      // Check if it's a timeout/connection error (simulated)
      // In a real browser env, network errors might show up differently.
      // For this logic, we assume if it fails, we offer retry.
      
      setErrorMsg(err.message)
      setStep("error")

      // If we want to auto-retry logic with countdown as requested:
      // "iniciar un contador de 10 segundos e indicamos al usuario que algo paso"
      if (retryCount < 1) { // Let's try once automatically
         startRetryCountdown()
      }
    }
  }

  const startRetryCountdown = () => {
    setCountdown(10)
    const interval = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(interval)
          handleValidation() // Retry
          setRetryCount(prevCount => prevCount + 1)
          return 0
        }
        return prev - 1
      })
    }, 1000)
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
           <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md flex items-start gap-2">
             <AlertCircle className="h-4 w-4 mt-0.5" />
             <div className="flex-1">
               <p className="font-medium">Error: {errorMsg}</p>
               {countdown > 0 && (
                 <p className="mt-1 text-slate-600">
                   Retrying connection in {countdown}s...
                 </p>
               )}
             </div>
           </div>
        )}

        <Button 
          className="w-full" 
          onClick={handleValidation}
          disabled={step === "validating" || countdown > 0 || !apiKey}
        >
          {step === "validating" ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Validating...
            </>
          ) : (
            "Validate & Save"
          )}
        </Button>
      </div>
    </div>
  )
}
