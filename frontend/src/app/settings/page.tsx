'use client'

import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { ApiKeysManager } from "@/components/api-keys-manager"
import { PreferencesForm } from "@/components/settings/preferences-form"
import { AdvancedSettings } from "@/components/settings/advanced-settings"

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Settings</h1>

        <Tabs defaultValue="providers">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="providers">Providers</TabsTrigger>
            <TabsTrigger value="general">General</TabsTrigger>
            <TabsTrigger value="advanced">Advanced</TabsTrigger>
          </TabsList>

          <TabsContent value="providers">
            <ApiKeysManager />
          </TabsContent>

          <TabsContent value="general">
            <PreferencesForm />
          </TabsContent>

          <TabsContent value="advanced">
            <AdvancedSettings />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
