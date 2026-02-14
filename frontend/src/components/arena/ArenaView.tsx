'use client';

import { useWorkflowStore } from '@/store/workflowStore';
import { PromptCard } from './PromptCard';
import { EvaluationChart } from './EvaluationChart';
import { Skeleton } from '@/components/ui/skeleton';

export function ArenaView() {
  const { variants, status } = useWorkflowStore();

  if (status === 'generating' || status === 'evaluating') {
      return (
        <div className="flex flex-col gap-6 w-full max-w-7xl mx-auto p-4">
           <div className="w-full h-[300px] bg-muted/10 rounded-xl animate-pulse" />
           <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                  <div key={i} className="flex flex-col h-[500px] border rounded-xl p-4 gap-4">
                      <Skeleton className="h-8 w-1/3" />
                      <Skeleton className="h-full w-full" />
                      <div className="flex gap-2">
                          <Skeleton className="h-12 w-1/3" />
                          <Skeleton className="h-12 w-1/3" />
                          <Skeleton className="h-12 w-1/3" />
                      </div>
                  </div>
              ))}
           </div>
        </div>
      );
  }

  if (!variants || variants.length === 0) {
      return null;
  }

  return (
    <div className="flex flex-col gap-8 w-full max-w-7xl mx-auto p-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
      
      <div className="flex flex-col md:flex-row gap-8 items-start">
        {/* Left: Chart/Stats */}
        <div className="w-full md:w-1/3 lg:w-1/4 sticky top-4">
             <EvaluationChart />
             <div className="mt-4 p-4 bg-muted/20 rounded-xl text-sm text-muted-foreground border border-dashed">
                <p>Compare the variants across Clarity, Safety, and Completeness. Edit any variant to refine it further.</p>
             </div>
        </div>

        {/* Right: Cards Grid */}
        <div className="flex-1 w-full">
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                {variants.map((variant, index) => (
                <PromptCard key={index} variant={variant} index={index} />
                ))}
            </div>
        </div>
      </div>

    </div>
  );
}
