import { TrendingUp, TrendingDown, Minus, Target, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

export interface IndexPrediction {
  name: string;
  futures?: string;
  direction: string;
  target: string;
  support: string;
  resistance: string;
  confidence: number;
  logic: string;
  keyEvents: string;
}

interface IndexPredictionCardProps {
  prediction: IndexPrediction;
}

export function IndexPredictionCard({ prediction }: IndexPredictionCardProps) {
  const directionIcon = prediction.direction.includes('偏多') || prediction.direction.includes('多')
    ? <TrendingUp className="w-4 h-4 text-positive" />
    : prediction.direction.includes('偏空') || prediction.direction.includes('空')
    ? <TrendingDown className="w-4 h-4 text-negative" />
    : <Minus className="w-4 h-4 text-foreground-subtle" />;

  return (
    <div className="bg-surface border border-border rounded-xl p-5 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h4 className="text-base font-semibold text-foreground">{prediction.name}</h4>
        <div className="flex items-center gap-2">
          {directionIcon}
          <span className={cn(
            "text-sm font-medium",
            prediction.direction.includes('多') ? "text-positive" :
            prediction.direction.includes('空') ? "text-negative" : "text-foreground-subtle"
          )}>
            {prediction.direction}
          </span>
        </div>
      </div>

      {/* Futures guide */}
      {prediction.futures && (
        <div className="flex items-center gap-2 text-sm">
          <span className="text-foreground-subtle">期货指引</span>
          <span className="font-mono text-foreground">{prediction.futures}</span>
        </div>
      )}

      {/* Price levels */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-surface-elevated/50 rounded-lg p-3">
          <div className="flex items-center gap-1.5 text-xs text-foreground-subtle mb-1">
            <Target className="w-3 h-3 text-positive" />
            目标
          </div>
          <p className="text-sm font-mono font-medium text-positive">{prediction.target}</p>
        </div>
        <div className="bg-surface-elevated/50 rounded-lg p-3">
          <div className="flex items-center gap-1.5 text-xs text-foreground-subtle mb-1">
            <TrendingDown className="w-3 h-3 text-negative" />
            支撑
          </div>
          <p className="text-sm font-mono font-medium text-negative">{prediction.support}</p>
        </div>
        <div className="bg-surface-elevated/50 rounded-lg p-3">
          <div className="flex items-center gap-1.5 text-xs text-foreground-subtle mb-1">
            <TrendingUp className="w-3 h-3 text-warning" />
            阻力
          </div>
          <p className="text-sm font-mono font-medium text-warning">{prediction.resistance}</p>
        </div>
      </div>

      {/* Confidence */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-foreground-subtle">置信度</span>
        <div className="flex gap-0.5">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className={cn(
                "w-4 h-1.5 rounded-full",
                i <= prediction.confidence ? "bg-primary" : "bg-border"
              )}
            />
          ))}
        </div>
        <span className="text-xs text-foreground-subtle">({prediction.confidence}/5)</span>
      </div>

      {/* Logic */}
      <div className="text-sm text-foreground-muted leading-relaxed">
        {prediction.logic}
      </div>

      {/* Key events */}
      <div className="flex items-start gap-2 text-xs text-foreground-subtle">
        <AlertTriangle className="w-3 h-3 mt-0.5 flex-shrink-0" />
        <span>关键事件：{prediction.keyEvents}</span>
      </div>
    </div>
  );
}
