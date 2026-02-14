"use client"

import { useEffect, useState } from "react"
import { OnboardingForm } from "@/components/onboarding-form"
import { Loader2 } from "lucide-react"

export default function Home() {
  const [loading, setLoading] = useState(true)
  const [configured, setConfigured] = useState(false)

  useEffect(() => {
    // Check if settings exist
    fetch("http://localhost:8001/api/settings")
      .then(res => res.json())
      .then(data => {
        if (data.configured) {
          setConfigured(true)
        }
      })
      .catch(err => {
        console.error("Backend not reachable", err)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
      </div>
    )
  }

  if (!configured) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-slate-50 p-4">
        <OnboardingForm />
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold">PromptForge Arena</h1>
        <p>System is configured and ready for Phase 2.</p>
      </div>
    </main>
  )
}
