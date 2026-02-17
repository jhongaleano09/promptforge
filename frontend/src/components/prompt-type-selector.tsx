'use client';

import { useState, useEffect } from 'react';
import { FileText, Settings, Image, Plus } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { API_BASE } from "@/config/api";

type PromptType = 'basic' | 'system' | 'image' | 'additional';

interface PromptTypeOption {
  id: PromptType;
  name: string;
  description: string;
  enabled: boolean;
  recommended_models: string[];
  tags: string[];
  category: string;
}

// Map Lucide Icons to prompt types
const ICON_MAP: Record<PromptType, typeof FileText> = {
  basic: FileText,
  system: Settings,
  image: Image,
  additional: Plus,
};

interface PromptTypeSelectorProps {
  selectedType: PromptType;
  onTypeSelect: (type: PromptType) => void;
  disabled?: boolean;
}

export function PromptTypeSelector({ 
  selectedType, 
  onTypeSelect, 
  disabled = false 
}: PromptTypeSelectorProps) {
  const { t } = useLanguage();
  const [availableTypes, setAvailableTypes] = useState<PromptTypeOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [showDisabledModal, setShowDisabledModal] = useState(false);
  const [selectedDisabled, setSelectedDisabled] = useState<PromptTypeOption | null>(null);

  useEffect(() => {
    fetchTypes();
  }, []);

  const fetchTypes = async () => {
    try {
      const res = await fetch(`${API_BASE}/prompts/types`);
      const data = await res.json();
      setAvailableTypes(data.types);
    } catch (error) {
      console.error('Error loading prompt types:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTypeClick = (type: PromptTypeOption) => {
    if (!type.enabled) {
      setSelectedDisabled(type);
      setShowDisabledModal(true);
      return;
    }
    
    onTypeSelect(type.id);
  };

  // Save to localStorage
  useEffect(() => {
    if (selectedType) {
      localStorage.setItem('promptforge_selected_type', selectedType);
    }
  }, [selectedType]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <>
      <div className="max-w-2xl mx-auto mb-8 space-y-4">
        <div className="space-y-2 text-center">
          <h3 className="text-lg font-semibold">{t('prompt_type_selector_title')}</h3>
          <p className="text-sm text-muted-foreground">{t('prompt_type_selector_description')}</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {availableTypes.map((type) => {
            const Icon = ICON_MAP[type.id as PromptType];
            const typeKey = `prompt_type_${type.id}`;
            
            return (
              <button
                key={type.id}
                disabled={disabled}
                onClick={() => handleTypeClick(type)}
                className={`
                  p-4 border rounded-lg text-left transition-all
                  ${selectedType === type.id 
                    ? 'border-primary bg-primary/5 ring-2 ring-primary' 
                    : 'border-border hover:border-primary/50'}
                  ${!type.enabled ? 'opacity-60' : ''}
                  ${disabled ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}
                `}
              >
                <div className="flex items-start gap-3">
                  {Icon && <Icon className="w-6 h-6 text-primary mt-0.5" />}
                  
                  <div className="flex-1">
                    <div className="font-semibold text-base">{t(`${typeKey}_name`)}</div>
                    <div className="text-sm text-muted-foreground mt-1">
                      {t(`${typeKey}_description`)}
                    </div>
                    
                    {!type.enabled && (
                      <div className="mt-2">
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-100">
                          🕐 {t('prompt_type_coming_soon_title')}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Modal for disabled types */}
      <Dialog open={showDisabledModal} onOpenChange={setShowDisabledModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t('prompt_type_coming_soon_title')}</DialogTitle>
            <DialogDescription>
              {t('prompt_type_coming_soon_description')}
            </DialogDescription>
          </DialogHeader>
          <div className="mt-4">
            <button
              onClick={() => setShowDisabledModal(false)}
              className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
            >
              {t('prompt_type_coming_soon_close')}
            </button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
