import React, { useEffect, useState } from 'react';
import { useWorkflowStore } from '@/store/workflowStore';
import { API_BASE } from '@/config/api';
import { useLanguage } from '@/contexts/LanguageContext';
import { Boxes, Cpu } from 'lucide-react';

interface ApiAndModelSelectorProps {
  className?: string;
}

export function ApiAndModelSelector({ className }: ApiAndModelSelectorProps) {
  const { t } = useLanguage();
  const [providers, setProviders] = useState<string[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [loadingProviders, setLoadingProviders] = useState(true);
  const [loadingModels, setLoadingModels] = useState(false);
  
  const { selectedProvider, setSelectedProvider, selectedModel, setSelectedModel } = useWorkflowStore();

  // Load Providers
  useEffect(() => {
    async function fetchProviders() {
      try {
        const res = await fetch(`${API_BASE}/settings/validate-active`);
        if (res.ok) {
          const data = await res.json();
          const activeProviders = data.active_providers || [];
          setProviders(activeProviders);

          if (activeProviders.length > 0) {
            if (!selectedProvider || !activeProviders.includes(selectedProvider)) {
              setSelectedProvider(activeProviders[0]);
            }
          } else {
             setSelectedProvider(null);
          }
        }
      } catch (error) {
        console.error('Error fetching providers:', error);
      } finally {
        setLoadingProviders(false);
      }
    }

    fetchProviders();
  }, [selectedProvider, setSelectedProvider]); // Only on mount, but added deps to satisfy linter

  // Load Models when Provider changes
  useEffect(() => {
    async function fetchModels() {
      if (!selectedProvider) {
        setModels([]);
        return;
      }
      setLoadingModels(true);
      try {
        const res = await fetch(`${API_BASE}/models?provider=${selectedProvider}`);
        if (res.ok) {
          const data = await res.json();
          setModels(data);
          
          if (data.length > 0) {
            // Set first model if none selected or if selected model is not in list
            if (!selectedModel || !data.includes(selectedModel)) {
              setSelectedModel(data[0]);
            }
          } else {
             setSelectedModel(null);
          }
        }
      } catch (error) {
        console.error('Error fetching models:', error);
        setModels([]);
      } finally {
        setLoadingModels(false);
      }
    }

    fetchModels();
  }, [selectedProvider, selectedModel, setSelectedModel]);

  if (loadingProviders) return <div className="text-xs text-muted-foreground">{t("provider_selector_loading")}</div>;

  if (providers.length === 0) {
    return (
      <div className={`text-xs text-destructive ${className}`}>
        {t("provider_selector_no_providers")}
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {/* Provider Selector */}
      <div className="flex items-center gap-1.5 bg-muted/30 rounded-lg p-1 border">
        <Boxes className="w-3.5 h-3.5 text-muted-foreground ml-1" />
        <select
          value={selectedProvider || ''}
          onChange={(e) => setSelectedProvider(e.target.value)}
          className="h-7 text-xs bg-transparent border-none focus-visible:outline-none focus-visible:ring-0 cursor-pointer text-muted-foreground font-medium"
        >
          {providers.map((p) => (
            <option key={p} value={p}>
              {p === 'openai' ? 'OpenAI' : p === 'anthropic' ? 'Anthropic' : p === 'ollama' ? 'Ollama' : p}
            </option>
          ))}
        </select>
      </div>

      {/* Model Selector */}
      {selectedProvider && (
        <div className="flex items-center gap-1.5 bg-muted/30 rounded-lg p-1 border">
          <Cpu className="w-3.5 h-3.5 text-muted-foreground ml-1" />
          <select
            value={selectedModel || ''}
            onChange={(e) => setSelectedModel(e.target.value)}
            disabled={loadingModels || models.length === 0}
            className="h-7 text-xs bg-transparent border-none focus-visible:outline-none focus-visible:ring-0 cursor-pointer font-medium min-w-[120px]"
          >
            {loadingModels ? (
              <option>Cargando modelos...</option>
            ) : models.length > 0 ? (
              models.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))
            ) : (
              <option>Sin modelos</option>
            )}
          </select>
        </div>
      )}
    </div>
  );
}
