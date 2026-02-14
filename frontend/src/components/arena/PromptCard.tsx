'use client';

import { useState } from 'react';
import { Copy, Download, Edit2, Check, X, Play, RefreshCw } from 'lucide-react';
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
  const { updateVariant, runTest, testResults, isTesting, refineVariant, isRefining } = useWorkflowStore();
  const [isEditing, setIsEditing] = useState(false);
  const [isTestingMode, setIsTestingMode] = useState(false);
  const [testInput, setTestInput] = useState('');
  const [editContent, setEditContent] = useState(variant.content);
  const [copied, setCopied] = useState(false);

  // For refinement
  const [isRefiningMode, setIsRefiningMode] = useState(false);
  const [refineFeedback, setRefineFeedback] = useState('');

  const handleSave = () => {
    updateVariant(index, editContent);
    setIsEditing(false);
  };

  const handleRunTest = async () => {
      if (!testInput) return;
      // We use variant.content (or editContent if saving logic is immediate, but let's use store variant)
      await runTest(variant.content, variant.id || String(index), testInput);
  };

  const handleRefine = async () => {
      if (!refineFeedback) return;
      await refineVariant(variant.id || String(index), refineFeedback);
      setIsRefiningMode(false);
      setRefineFeedback('');
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
            <Button size="icon" variant={isTestingMode ? "secondary" : "ghost"} className="h-7 w-7" onClick={() => setIsTestingMode(!isTestingMode)} title="Test Prompt">
                <Play className="w-3.5 h-3.5" />
            </Button>
            <Button size="icon" variant={isRefiningMode ? "secondary" : "ghost"} className="h-7 w-7" onClick={() => setIsRefiningMode(!isRefiningMode)} title="Refine">
                <RefreshCw className="w-3.5 h-3.5" />
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
        ) : isTestingMode ? (
            <div className="flex flex-col gap-4 h-full">
                <div className="text-xs font-semibold text-muted-foreground uppercase">Test Input</div>
                <Textarea 
                    placeholder="Enter test input (e.g. user message)..."
                    value={testInput}
                    onChange={(e) => setTestInput(e.target.value)}
                    className="min-h-[100px] resize-none text-xs"
                />
                <Button size="sm" onClick={handleRunTest} disabled={isTesting || !testInput}>
                    {isTesting ? "Running..." : "Run Test"}
                </Button>
                
                {testResults?.[variant.id || String(index)] && (
                    <div className="flex-1 flex flex-col gap-2 min-h-0">
                        <div className="text-xs font-semibold text-muted-foreground uppercase border-t pt-2">Output</div>
                        <div className="bg-muted/30 p-2 rounded text-xs font-mono overflow-y-auto flex-1">
                            {testResults[variant.id || String(index)]}
                        </div>
                    </div>
                )}
            </div>
        ) : isRefiningMode ? (
            <div className="flex flex-col gap-4 h-full">
                <div className="text-xs font-semibold text-muted-foreground uppercase">Refine Prompt</div>
                <div className="text-xs text-muted-foreground">
                    Describe how you want to improve this specific variant. This will generate 3 new variations based on it.
                </div>
                <Textarea 
                    placeholder="E.g. Make it shorter, use a more formal tone..."
                    value={refineFeedback}
                    onChange={(e) => setRefineFeedback(e.target.value)}
                    className="min-h-[100px] resize-none text-xs"
                />
                <Button size="sm" onClick={handleRefine} disabled={isRefining || !refineFeedback}>
                    {isRefining ? "Refining..." : "Generate Variations"}
                </Button>
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
