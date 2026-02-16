import React, { useEffect, useState } from 'react';
import { useWorkflowStore } from '@/store/workflowStore';
import { API_BASE } from '@/config/api';

interface ProviderSelectorProps {
  className?: string;
}

export function ProviderSelector({ className }: ProviderSelectorProps) {
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

  if (loading) return <div className="text-xs text-muted-foreground">Loading providers...</div>;

  if (providers.length === 0) {
    return (
      <div className={`text-xs text-destructive ${className}`}>
        No active providers configured. Please go to Settings.
      </div>
    );
  }

  if (providers.length === 1) {
    return (
      <div className={`text-xs text-muted-foreground ${className}`}>
        Using <strong>{providers[0]}</strong>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-xs text-muted-foreground whitespace-nowrap">Provider:</span>
      <select
        value={selectedProvider || ''}
        onChange={(e) => setSelectedProvider(e.target.value)}
        className="h-8 text-xs rounded-md border border-input bg-background px-3 py-1 shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
      >
        {providers.map((p) => (
          <option key={p} value={p}>
            {p.charAt(0).toUpperCase() + p.slice(1)}
          </option>
        ))}
      </select>
    </div>
  );
}
