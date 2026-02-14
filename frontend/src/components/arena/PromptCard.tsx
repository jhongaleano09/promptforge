'use client';

import { useState } from 'react';
import { Copy, Download, Edit2, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Variant, useWorkflowStore } from '@/store/workflowStore';
import ReactMarkdown from 'react-markdown';

interface PromptCardProps {
  variant: Variant;
  index: number;
}

export function PromptCard({ variant, index }: PromptCardProps) {
  const { updateVariant } = useWorkflowStore();
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(variant.content);
  const [copied, setCopied] = useState(false);

  const handleSave = () => {
    updateVariant(index, editContent);
    setIsEditing(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(variant.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExport = () => {
    const blob = new Blob([variant.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `prompt-variant-${index + 1}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Safe access to evaluation metrics
  const clarity = variant.evaluation?.clarity ?? 0;
  const safety = variant.evaluation?.safety ?? 0;
  const completeness = variant.evaluation?.completeness ?? 0;

  return (
    <div className="flex flex-col border rounded-xl bg-card shadow-sm h-full overflow-hidden transition-all hover:shadow-md">
      <div className="p-3 border-b flex items-center justify-between bg-muted/30">
        <div className="flex items-center gap-2">
           <Badge variant="secondary" className="font-mono">Var {String.fromCharCode(65 + index)}</Badge>
           {variant.model_used && <span className="text-xs text-muted-foreground">{variant.model_used}</span>}
        </div>
        <div className="flex gap-1">
            <Button size="icon" variant="ghost" className="h-7 w-7" onClick={handleCopy} title="Copy">
                {copied ? <Check className="w-3.5 h-3.5 text-green-500" /> : <Copy className="w-3.5 h-3.5" />}
            </Button>
            <Button size="icon" variant="ghost" className="h-7 w-7" onClick={handleExport} title="Export .txt">
                <Download className="w-3.5 h-3.5" />
            </Button>
             <Button size="icon" variant="ghost" className="h-7 w-7" onClick={() => setIsEditing(!isEditing)} title="Edit">
                <Edit2 className="w-3.5 h-3.5" />
            </Button>
        </div>
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto min-h-[350px] max-h-[500px] text-sm bg-background relative">
        {isEditing ? (
            <div className="h-full flex flex-col gap-2">
                <Textarea 
                    value={editContent} 
                    onChange={(e) => setEditContent(e.target.value)} 
                    className="flex-1 font-mono text-xs resize-none bg-muted/50"
                />
                <div className="flex justify-end gap-2">
                    <Button size="sm" variant="ghost" onClick={() => setIsEditing(false)}>Cancel</Button>
                    <Button size="sm" onClick={handleSave}>Save Changes</Button>
                </div>
            </div>
        ) : (
            <div className="prose dark:prose-invert prose-sm max-w-none">
               <ReactMarkdown>{variant.content}</ReactMarkdown>
            </div>
        )}
      </div>

      {/* Mini Scoreboard */}
      <div className="p-3 border-t bg-muted/10 grid grid-cols-3 gap-px text-center text-xs divide-x">
         <div className="flex flex-col gap-1">
            <span className="text-muted-foreground uppercase tracking-wider text-[10px]">Clarity</span>
            <div className="font-bold text-blue-500">{clarity}/10</div>
         </div>
         <div className="flex flex-col gap-1">
            <span className="text-muted-foreground uppercase tracking-wider text-[10px]">Safety</span>
            <div className="font-bold text-green-500">{safety}/10</div>
         </div>
         <div className="flex flex-col gap-1">
            <span className="text-muted-foreground uppercase tracking-wider text-[10px]">Completeness</span>
            <div className="font-bold text-purple-500">{completeness}/10</div>
         </div>
      </div>
    </div>
  );
}
