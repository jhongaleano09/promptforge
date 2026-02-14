'use client';

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts';
import { useWorkflowStore } from '@/store/workflowStore';

export function EvaluationChart() {
  const { variants } = useWorkflowStore();

  if (!variants || variants.length === 0) {
      return (
          <div className="flex items-center justify-center h-[300px] text-muted-foreground bg-muted/20 rounded-xl border border-dashed">
              No evaluation data yet
          </div>
      );
  }

  const data = [
    { subject: 'Clarity', fullMark: 10 },
    { subject: 'Safety', fullMark: 10 },
    { subject: 'Completeness', fullMark: 10 },
  ];

  variants.forEach((v, i) => {
    const key = `Variant ${String.fromCharCode(65 + i)}`;
    const evalData = v.evaluation || { clarity: 0, safety: 0, completeness: 0 };
    
    // @ts-ignore - dynamic assignment
    data[0][key] = evalData.clarity;
    // @ts-ignore
    data[1][key] = evalData.safety;
    // @ts-ignore
    data[2][key] = evalData.completeness;
  });

  const colors = ['#3b82f6', '#10b981', '#a855f7']; // blue, green, purple

  return (
    <div className="w-full h-[350px] bg-card rounded-xl border shadow-sm p-4">
      <h3 className="text-sm font-medium mb-4 text-center text-muted-foreground">Evaluation Radar</h3>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="currentColor" className="text-muted/20" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: 'currentColor', fontSize: 11 }} className="text-muted-foreground" />
          <PolarRadiusAxis angle={30} domain={[0, 10]} tick={false} axisLine={false} />
          
          {variants.map((v, i) => (
             <Radar
                key={i}
                name={`Var ${String.fromCharCode(65 + i)}`}
                dataKey={`Variant ${String.fromCharCode(65 + i)}`}
                stroke={colors[i % colors.length]}
                fill={colors[i % colors.length]}
                fillOpacity={0.2}
             />
          ))}
          <Legend />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            itemStyle={{ fontSize: '12px' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
