import { create } from 'zustand';
import { fetchEventSource } from '@microsoft/fetch-event-source';

export interface Variant {
  title: string; // e.g., "Variant A"
  content: string;
  model_used?: string;
  evaluation?: {
    clarity: number;
    safety: number;
    completeness: number;
    average: number;
    feedback: string;
  };
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface WorkflowState {
  threadId: string | null;
  status: 'idle' | 'clarifying' | 'generating' | 'evaluating' | 'completed' | 'error';
  messages: Message[];
  variants: Variant[];
  currentStreamingMessage: string;
  evaluations: any;
  error: string | null;
  activeTab: string;

  startWorkflow: (input: string) => Promise<void>;
  answerClarification: (answer: string) => Promise<void>;
  updateVariant: (index: number, content: string) => void;
  setActiveTab: (tab: string) => void;
  reset: () => void;
}

const API_BASE = 'http://localhost:8000/api';

export const useWorkflowStore = create<WorkflowState>((set, get) => ({
  threadId: null,
  status: 'idle',
  messages: [],
  variants: [],
  currentStreamingMessage: '',
  evaluations: {},
  error: null,
  activeTab: 'chat',

  startWorkflow: async (input: string) => {
    set({ status: 'clarifying', error: null, currentStreamingMessage: '', messages: [{ role: 'user', content: input }] });

    try {
      await fetchEventSource(`${API_BASE}/workflow/stream/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: input }),
        onmessage(ev) {
          const { event, data } = ev;
          const parsedData = JSON.parse(data);

          if (event === 'metadata') {
            set({ threadId: parsedData.thread_id });
          } else if (event === 'token') {
            set((state) => ({
              currentStreamingMessage: state.currentStreamingMessage + parsedData.content
            }));
          } else if (event === 'status') {
             // Map backend status to frontend status
             const backendStatus = parsedData.status; // clarify, generate, evaluate
             let frontendStatus: WorkflowState['status'] = 'clarifying';
             if (backendStatus === 'generate') frontendStatus = 'generating';
             if (backendStatus === 'evaluate') frontendStatus = 'evaluating';
             
             set({ status: frontendStatus });
          } else if (event === 'update') {
            // Full state update
            const { status, message, questions, variants, evaluations } = parsedData;
            
            // If we have a final message (clarification question), append it to messages
            // But we might have been streaming it into currentStreamingMessage
            // So we should commit currentStreamingMessage to messages if it's done
            
            set((state) => {
                const newMessages = [...state.messages];
                if (state.currentStreamingMessage) {
                    newMessages.push({ role: 'assistant', content: state.currentStreamingMessage });
                } else if (message && (!newMessages.length || newMessages[newMessages.length - 1].role !== 'assistant')) {
                    // Fallback if no streaming happened but we got a message
                    newMessages.push({ role: 'assistant', content: message });
                }
                
                // If status is completed, switch tab to arena
                const nextTab = status === 'completed' ? 'arena' : state.activeTab;

                return {
                    status: status === 'completed' ? 'completed' : 'clarifying', // or keep current if waiting
                    messages: newMessages,
                    currentStreamingMessage: '',
                    variants: variants || state.variants,
                    evaluations: evaluations || state.evaluations,
                    activeTab: nextTab
                };
            });
          } else if (event === 'error') {
            set({ error: parsedData.detail, status: 'error' });
          }
        },
        onerror(err) {
            console.error("SSE Error:", err);
            // Don't throw to avoid retrying indefinitely in this simple logic, 
            // unless we want auto-reconnect. For this prototype, maybe just log and stop.
            set({ error: "Connection lost" });
            throw err; // rethrow to stop
        }
      });
    } catch (e: any) {
        set({ error: e.message || "Failed to start workflow" });
    }
  },

  answerClarification: async (answer: string) => {
    const { threadId } = get();
    if (!threadId) return;

    set((state) => ({ 
        messages: [...state.messages, { role: 'user', content: answer }],
        currentStreamingMessage: '',
        status: 'clarifying' // Assume we go back to clarifying or next step
    }));

    try {
      await fetchEventSource(`${API_BASE}/workflow/stream/${threadId}/answer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answer }),
        onmessage(ev) {
            const { event, data } = ev;
            const parsedData = JSON.parse(data);
  
            if (event === 'token') {
              set((state) => ({
                currentStreamingMessage: state.currentStreamingMessage + parsedData.content
              }));
            } else if (event === 'status') {
                const backendStatus = parsedData.status;
                let frontendStatus: WorkflowState['status'] = 'clarifying';
                if (backendStatus === 'generate') frontendStatus = 'generating';
                if (backendStatus === 'evaluate') frontendStatus = 'evaluating';
                set({ status: frontendStatus });
            } else if (event === 'update') {
              const { status, message, variants, evaluations } = parsedData;
              
              set((state) => {
                  const newMessages = [...state.messages];
                  if (state.currentStreamingMessage) {
                      newMessages.push({ role: 'assistant', content: state.currentStreamingMessage });
                  }
                  
                  const nextTab = status === 'completed' ? 'arena' : state.activeTab;

                  return {
                      status: status === 'completed' ? 'completed' : 'clarifying',
                      messages: newMessages,
                      currentStreamingMessage: '',
                      variants: variants || state.variants,
                      evaluations: evaluations || state.evaluations,
                      activeTab: nextTab
                  };
              });
            } else if (event === 'error') {
                set({ error: parsedData.detail, status: 'error' });
            }
        },
        onerror(err) {
            console.error("SSE Error:", err);
            throw err;
        }
      });
    } catch (e: any) {
        set({ error: e.message || "Failed to submit answer" });
    }
  },

  updateVariant: (index, content) => {
    set((state) => {
        const newVariants = [...state.variants];
        if (newVariants[index]) {
            newVariants[index] = { ...newVariants[index], content };
        }
        return { variants: newVariants };
    });
  },

  setActiveTab: (tab) => set({ activeTab: tab }),
  reset: () => set({ threadId: null, status: 'idle', messages: [], variants: [], evaluations: {}, error: null, currentStreamingMessage: '' })
}));
