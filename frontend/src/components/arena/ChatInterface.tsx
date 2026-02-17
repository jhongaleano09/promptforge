'use client';

import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useWorkflowStore } from '@/store/workflowStore';
import { cn } from '@/lib/utils';
import { useLanguage } from '@/contexts/LanguageContext';

export function ChatInterface() {
  const { t } = useLanguage();
  const { messages, currentStreamingMessage, answerClarification, status } = useWorkflowStore();
  const [input, setInput] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentStreamingMessage]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || (status !== 'clarifying' && status !== 'idle')) return;
    answerClarification(input);
    setInput('');
  };

  const isLocked = status === 'generating' || status === 'evaluating' || status === 'completed';

  return (
    <div className="flex flex-col h-[600px] w-full max-w-3xl mx-auto border rounded-xl bg-background shadow-sm overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b bg-muted/30 flex items-center justify-between">
        <h3 className="font-semibold flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary" />
          {t("chat_assistant_title")}
        </h3>
        {status !== 'idle' && status !== 'clarifying' && status !== 'completed' && status !== 'error' && (
            <span className="text-xs text-muted-foreground flex items-center gap-1">
                <Loader2 className="w-3 h-3 animate-spin" />
                {status === 'generating' ? t("chat_status_generating") : t("chat_status_evaluating")}
            </span>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
              "flex w-full",
              msg.role === 'user' ? "justify-end" : "justify-start"
            )}
          >
            <div className={cn(
              "max-w-[85%] rounded-lg px-4 py-3 text-sm shadow-sm prose dark:prose-invert prose-p:my-1 prose-ul:my-1",
              msg.role === 'user' 
                ? "bg-primary text-primary-foreground rounded-tr-none" 
                : "bg-muted text-foreground rounded-tl-none border"
            )}>
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </motion.div>
        ))}
        
        {currentStreamingMessage && (
            <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex w-full justify-start"
          >
            <div className="max-w-[85%] rounded-lg px-4 py-3 text-sm bg-muted text-foreground rounded-tl-none border shadow-sm prose dark:prose-invert">
              <ReactMarkdown>{currentStreamingMessage}</ReactMarkdown>
              <span className="inline-block w-1.5 h-4 ml-1 align-middle bg-primary animate-pulse"/>
            </div>
          </motion.div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t bg-background">
        <div className="flex gap-2">
          <Input 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={isLocked ? t("chat_processing") : t("chat_input_placeholder")}
            disabled={isLocked}
            className="flex-1"
            autoFocus
          />
          <Button type="submit" disabled={!input.trim() || isLocked}>
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </form>
    </div>
  );
}
