'use client'

import * as React from "react"
import { cn } from "@/lib/utils"

interface SliderProps {
  value: number[]
  onValueChange: (value: number[]) => void
  min: number
  max: number
  step: number
  disabled?: boolean
  className?: string
}

export function Slider({
  value,
  onValueChange,
  min,
  max,
  step,
  disabled = false,
  className
}: SliderProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseFloat(e.target.value)
    onValueChange([newValue])
  }

  const percentage = ((value[0] - min) / (max - min)) * 100

  return (
    <div className={cn("relative w-full h-5", className)}>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value[0]}
        onChange={handleChange}
        disabled={disabled}
        className={cn(
          "absolute inset-0 w-full h-full opacity-0 cursor-pointer",
          "focus-visible:outline-none",
          disabled && "cursor-not-allowed"
        )}
      />
      <div className="absolute inset-0 h-2 bg-input rounded-full overflow-hidden">
        <div
          className="absolute left-0 top-0 h-full bg-primary rounded-full transition-all"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div
        className={cn(
          "absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-background border-2 border-primary rounded-full shadow-sm transition-all",
          "pointer-events-none",
          disabled && "opacity-50"
        )}
        style={{ left: `calc(${percentage}% - 8px)` }}
      />
    </div>
  )
}
