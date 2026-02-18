'use client'

import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { ApiKeysManager } from "@/components/api-keys-manager"
import { PreferencesForm } from "@/components/settings/preferences-form"
import { AdvancedSettings } from "@/components/settings/advanced-settings"
import { useLanguage } from "@/contexts/LanguageContext"

export default function SettingsPage() {
  const { t } = useLanguage()

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">{t("settings")}</h1>

        <Tabs defaultValue="providers">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="providers">{t("settings_page_providers")}</TabsTrigger>
            <TabsTrigger value="general">{t("settings_page_general")}</TabsTrigger>
            <TabsTrigger value="advanced">{t("settings_page_advanced")}</TabsTrigger>
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
