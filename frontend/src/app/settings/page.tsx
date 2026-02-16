import { ApiKeysManager } from "@/components/api-keys-manager"

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Settings</h1>
        <ApiKeysManager />
      </div>
    </div>
  )
}
