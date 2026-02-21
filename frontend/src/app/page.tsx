'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { OnboardingForm } from '@/components/onboarding-form';
import { ChatInterface } from '@/components/arena/ChatInterface';
import { ArenaView } from '@/components/arena/ArenaView';
import { useWorkflowStore } from '@/store/workflowStore';
import { ApiAndModelSelector } from '@/components/api-and-model-selector';
import { PromptTypeSelector } from '@/components/prompt-type-selector';
import { cn } from '@/lib/utils';
import { LayoutDashboard, MessageSquare, Sparkles, Sun, Moon, Settings as SettingsIcon } from 'lucide-react';
import { useTheme } from "next-themes";
import { API_BASE } from "@/config/api";
import { useLanguage } from "@/contexts/LanguageContext";

export default function Home() {
  const { t } = useLanguage();
  const router = useRouter();
  const { status, activeTab, setActiveTab, startWorkflow, error, reset } = useWorkflowStore();
  const [apiKeyConfigured, setApiKeyConfigured] = useState(false);
  const [loading, setLoading] = useState(true);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [promptType, setPromptType] = useState<any>('basic');
  const { theme, setTheme } = useTheme();

  // Handle mounting for theme to avoid hydration mismatch
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  // Load prompt type from localStorage on mount
  useEffect(() => {
    const savedType = localStorage.getItem('promptforge_prompt_type');
    if (savedType) {
      setPromptType(savedType);
    }
  }, []);

  useEffect(() => {
    // Check if configured and validate active keys
    validateConfiguration();
  }, []);

  const validateConfiguration = async () => {
    setLoading(true);
    setValidationError(null);

    try {
      const res = await fetch(`${API_BASE}/settings/validate-active`);
      const data = await res.json();

      if (data.has_active_key) {
        setApiKeyConfigured(true);
      } else {
        setApiKeyConfigured(false);
        if (data.warning) {
          console.log('Validation warning:', data.warning);
        }
      }
    } catch (err: any) {
      console.error('Validation error:', err);
      setValidationError(err.message || 'Failed to validate configuration');
      // Still try to show the app even if validation fails
      setApiKeyConfigured(true);
    } finally {
      setLoading(false);
    }
  };

  const showArena = status === 'completed' || status === 'generating' || status === 'evaluating';

  if (loading) {
      return <div className="min-h-screen flex items-center justify-center">{t("loading")}</div>;
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-4 md:p-8 bg-background text-foreground selection:bg-primary/20">

      {/* Header */}
      <header className="w-full max-w-7xl mb-8 flex justify-between items-center border-b pb-4">
         <button 
            onClick={() => reset()} 
            className="flex items-center gap-2 hover:opacity-80 transition-opacity text-left"
         >
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-primary-foreground" />
              </div>
               <h1 className="text-xl font-bold tracking-tight">{t("app_title")}</h1>
         </button>
          <div className="flex items-center gap-2">
             <button
                 onClick={() => router.push('/settings')}
                 className="p-2 rounded-lg hover:bg-muted transition-colors"
                 title={t("settings")}
             >
                 <SettingsIcon className="w-5 h-5" />
             </button>
             {mounted && (
                 <button
                     onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                     className="p-2 rounded-lg hover:bg-muted transition-colors"
                     title={t("toggle_theme")}
                 >
                     {theme === "dark" ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                 </button>
             )}
          </div>
      </header>

      {/* Main Content */}
      <div className="w-full max-w-7xl flex-1 flex flex-col">
        
        {!apiKeyConfigured ? (
             <div className="max-w-md mx-auto mt-20 w-full">
                <OnboardingForm />
                <div className="mt-4 text-center">
                    <button onClick={() => setApiKeyConfigured(true)} className="text-xs text-muted-foreground underline">
                        {t("onboarding_already_configured")}
                    </button>
                </div>
             </div>
        ) : (
             <div className="w-full flex flex-col gap-6">
                {/* Tabs Navigation */}
                {status !== 'idle' && (
                    <div className="flex justify-center">
                        <div className="bg-muted/50 p-1 rounded-xl flex gap-1 border">
                            <button 
                                onClick={() => setActiveTab('chat')}
                                className={cn(
                                    "px-6 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2",
                                    activeTab === 'chat' ? "bg-background shadow-sm text-foreground ring-1 ring-border" : "text-muted-foreground hover:text-foreground"
                                )}
                            >
                                <MessageSquare className="w-4 h-4" />
                                {t("home_tab_clarification")}
                            </button>
                            <button 
                                onClick={() => setActiveTab('arena')}
                                disabled={!showArena}
                                className={cn(
                                    "px-6 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2",
                                    activeTab === 'arena' ? "bg-background shadow-sm text-foreground ring-1 ring-border" : "text-muted-foreground hover:text-foreground",
                                    !showArena && "opacity-50 cursor-not-allowed"
                                )}
                            >
                                <LayoutDashboard className="w-4 h-4" />
                                {t("home_tab_arena")}
                            </button>
                        </div>
                    </div>
                )}

                {/* Content */}
                <div className="w-full">
                    {activeTab === 'chat' && (
                        <div className="w-full animate-in fade-in slide-in-from-bottom-2 duration-500">
                             {status === 'idle' ? (
                                 <>
                                   <PromptTypeSelector 
                                     selectedType={promptType}
                                     onTypeSelect={(type) => setPromptType(type)}
                                   />
                                   <InitialPromptInput 
                                     onSubmit={(text) => startWorkflow(text, promptType)} 
                                   />
                                 </>
                             ) : (
                                 <ChatInterface />
                             )}
                        </div>
                    )}
                    
                    {activeTab === 'arena' && (
                        <ArenaView />
                    )}
                </div>
             </div>
        )}
      </div>
      
      {error && (
        <div className="fixed bottom-6 right-6 bg-destructive text-destructive-foreground p-4 rounded-xl shadow-lg border animate-in slide-in-from-bottom-full duration-300">
            <p className="font-semibold">{t("error_occurred")}</p>
            <p className="text-sm opacity-90">{error}</p>
        </div>
      )}
    </main>
  );
}

function InitialPromptInput({ onSubmit }: { onSubmit: (text: string) => void }) {
    const { t } = useLanguage();
    const [text, setText] = useState('');
    return (
        <div className="max-w-2xl mx-auto mt-16 text-center space-y-8 animate-in zoom-in-95 duration-500">
            <div className="space-y-2">
                <h2 className="text-4xl font-extrabold tracking-tight lg:text-5xl">{t("home_what_build_title")}</h2>
                <p className="text-xl text-muted-foreground">{t("home_what_build_description")}</p>
            </div>
            
            <div className="flex flex-col gap-4 p-1 bg-gradient-to-br from-primary/20 via-primary/10 to-transparent rounded-2xl">
                <div className="bg-card rounded-xl p-2 shadow-sm border">
                    <div className="px-4 py-2 border-b flex justify-start items-center bg-muted/20 rounded-t-lg mb-2">
                        <span className="text-xs font-medium text-muted-foreground">{t("home_system_context")}</span>
                    </div>
                    <textarea 
                        className="w-full p-4 rounded-lg bg-transparent border-none outline-none resize-none text-lg min-h-[150px] placeholder:text-muted-foreground/50"
                        placeholder={t("home_input_placeholder")}
                        value={text}
                        onChange={e => setText(e.target.value)}
                        autoFocus
                    />
                    <div className="flex justify-between items-center pt-3 pb-1 px-2 border-t mt-2">
                        <ApiAndModelSelector />
                        <button 
                            onClick={() => onSubmit(text)}
                            disabled={!text.trim()}
                            className="px-8 py-2.5 bg-primary text-primary-foreground rounded-lg font-semibold hover:opacity-90 transition-all disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-primary/20"
                        >
                            <Sparkles className="w-4 h-4" />
                            {t("home_start_forging")}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
