import React, { useEffect, useState } from 'react';
import { useWorkflowStore } from '@/store/workflowStore';
import { API_BASE } from '@/config/api';
import { useLanguage } from '@/contexts/LanguageContext';

interface ProviderSelectorProps {
  className?: string;
}

export function ProviderSelector({ className }: ProviderSelectorProps) {
  const { t } = useLanguage();
  const [providers, setProviders] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const { selectedProvider, setSelectedProvider } = useWorkflowStore();

  useEffect(() => {
    async function fetchProviders() {
      try {
        const res = await fetch(`${API_BASE}/settings/validate-active`);
        if (res.ok) {
          const data = await res.json();
          const activeProviders = data.active_providers || [];
          setProviders(activeProviders);

          // Auto-select if only one provider and none selected, or if current selection is invalid
          if (activeProviders.length > 0) {
            if (!selectedProvider || !activeProviders.includes(selectedProvider)) {
              setSelectedProvider(activeProviders[0]);
            }
          } else {
             // No active providers
             setSelectedProvider(null);
          }
        }
      } catch (error) {
        console.error('Error fetching providers:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchProviders();
  }, [selectedProvider, setSelectedProvider]);

  if (loading) return <div className="text-xs text-muted-foreground">{t("provider_selector_loading")}</div>;

  if (providers.length === 0) {
    return (
      <div className={`text-xs text-destructive ${className}`}>
        {t("provider_selector_no_providers")}
      </div>
    );
  }

  if (providers.length === 1) {
    return (
      <div className={`text-xs text-muted-foreground ${className}`}>
        {t("provider_selector_using")} <strong>{providers[0]}</strong>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-xs text-muted-foreground whitespace-nowrap">{t("provider_selector_provider_label")}</span>
      <select
        value={selectedProvider || ''}
        onChange={(e) => setSelectedProvider(e.target.value)}
        className="h-8 text-xs rounded-md border border-input bg-background px-3 py-1 shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
      >
        {providers.map((p) => (
          <option key={p} value={p}>
            {p === 'openai' ? t("provider_selector_openai") : p === 'anthropic' ? t("provider_selector_anthropic") : t("provider_selector_ollama")}
          </option>
        ))}
      </select>
    </div>
  );
}
