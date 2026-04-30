import { TrendingUp, TrendingDown, Minus, Target, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export interface StockAnalysis {
  ticker: string;
  name: string;
  price?: string;
  change?: string;
  news: string;
  sentiment: 'bullish' | 'bearish' | 'neutral' | 'cautious';
  technical: string;
  catalyst: string;
  strategy: string;
  target?: string;
  stopLoss?: string;
}

interface StockAnalysisCardProps {
  stock: StockAnalysis;
}

export function StockAnalysisCard({ stock }: StockAnalysisCardProps) {
  const sentimentConfig = {
    bullish: { label: '偏多', color: 'text-positive', bg: 'bg-positive/10', icon: <TrendingUp className="w-3 h-3" /> },
    bearish: { label: '偏空', color: 'text-negative', bg: 'bg-negative/10', icon: <TrendingDown className="w-3 h-3" /> },
    neutral: { label: '中性', color: 'text-foreground-subtle', bg: 'bg-foreground-subtle/10', icon: <Minus className="w-3 h-3" /> },
    cautious: { label: '谨慎', color: 'text-warning', bg: 'bg-warning/10', icon: <AlertCircle className="w-3 h-3" /> },
  };

  const sentiment = sentimentConfig[stock.sentiment];

  return (
    <div className="bg-surface border border-border rounded-xl p-5 space-y-3 hover:border-border-hover transition-colors duration-200">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-surface-elevated rounded-lg px-2.5 py-1">
            <span className="text-sm font-mono font-semibold text-foreground">{stock.ticker}</span>
          </div>
          <span className="text-sm text-foreground-muted">{stock.name}</span>
        </div>
        {stock.price && (
          <div className="text-right">
            <p className="text-sm font-mono font-medium text-foreground">{stock.price}</p>
            {stock.change && (
              <p className={cn(
                "text-xs font-mono",
                stock.change.startsWith('+') ? "text-positive" :
                stock.change.startsWith('-') ? "text-negative" : "text-foreground-subtle"
              )}>
                {stock.change}
              </p>
            )}
          </div>
        )}
      </div>

      {/* Sentiment badge */}
      <div className="flex items-center gap-2">
        <span className={cn("text-xs font-medium px-2 py-0.5 rounded-md flex items-center gap-1", sentiment.bg, sentiment.color)}>
          {sentiment.icon}
          {sentiment.label}
        </span>
      </div>

      {/* News */}
      <p className="text-sm text-foreground-muted leading-relaxed">
        {stock.news}
      </p>

      {/* Technical */}
      <div className="text-xs text-foreground-subtle">
        <span className="text-foreground-muted font-medium">技术面：</span>
        {stock.technical}
      </div>

      {/* Catalyst */}
      <div className="text-xs text-foreground-subtle">
        <span className="text-foreground-muted font-medium">催化剂：</span>
        {stock.catalyst}
      </div>

      {/* Strategy */}
      <div className="text-xs text-foreground-muted font-medium">
        策略：{stock.strategy}
      </div>

      {/* Target & Stop Loss */}
      {(stock.target || stock.stopLoss) && (
        <div className="flex items-center gap-4 pt-2 border-t border-border">
          {stock.target && (
            <div className="flex items-center gap-1.5 text-xs">
              <Target className="w-3 h-3 text-positive" />
              <span className="text-foreground-subtle">目标</span>
              <span className="font-mono font-medium text-positive">{stock.target}</span>
            </div>
          )}
          {stock.stopLoss && (
            <div className="flex items-center gap-1.5 text-xs">
              <AlertCircle className="w-3 h-3 text-negative" />
              <span className="text-foreground-subtle">止损</span>
              <span className="font-mono font-medium text-negative">{stock.stopLoss}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
