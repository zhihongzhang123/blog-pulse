"use client";

import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, AlertTriangle, Eye, Activity, Target } from "lucide-react";

interface MarketIndicator {
  key: string;
  name: string;
  value: string;
  change: number;
  signal: "bullish" | "bearish" | "neutral" | "warning";
  comment: string;
}

interface MarketIndicatorsProps {
  indicators: MarketIndicator[];
  marketWidth: number;
  trendStatus: string;
  topConstruction: boolean;
  fomoGap: boolean;
  liquidityAlert: boolean;
}

const signalConfig = {
  bullish: { color: "text-positive", bg: "bg-positive/10", icon: TrendingUp },
  bearish: { color: "text-negative", bg: "bg-negative/10", icon: TrendingDown },
  neutral: { color: "text-foreground-muted", bg: "bg-foreground-muted/10", icon: Activity },
  warning: { color: "text-warning", bg: "bg-warning/10", icon: AlertTriangle },
};

export function MarketIndicators({ indicators, marketWidth, trendStatus, topConstruction, fomoGap, liquidityAlert }: MarketIndicatorsProps) {
  return (
    <div className="space-y-6">
      {/* 核心指标矩阵 */}
      <div>
        <h3 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-4">
          <Eye className="w-4 h-4 text-primary" />
          核心指标矩阵
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {indicators.map((indicator) => {
            const config = signalConfig[indicator.signal];
            const Icon = config.icon;
            return (
              <div
                key={indicator.key}
                className="bg-surface-elevated/30 border border-border rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-foreground-subtle">{indicator.name}</span>
                  <span className={cn("text-xs font-semibold px-2 py-0.5 rounded-md", config.bg, config.color)}>
                    <Icon className="w-3 h-3 inline mr-1" />
                    {indicator.signal === "bullish" ? "偏多" : indicator.signal === "bearish" ? "偏空" : indicator.signal === "warning" ? "警示" : "中性"}
                  </span>
                </div>
                <p className="text-lg font-mono font-semibold text-foreground tracking-tight mb-1">
                  {indicator.value}
                </p>
                <p className={cn("text-xs font-medium", indicator.change >= 0 ? "text-positive" : "text-negative")}>
                  {indicator.change > 0 ? "+" : ""}{indicator.change.toFixed(2)}%
                </p>
                <p className="text-xs text-foreground-muted mt-2 leading-relaxed">
                  {indicator.comment}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* 市场结构诊断 */}
      <div>
        <h3 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-4">
          <Target className="w-4 h-4 text-primary" />
          市场结构诊断
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* 市场宽度 */}
          <div className="bg-surface-elevated/30 border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-foreground-subtle">市场宽度</span>
              <span className={cn("text-xs font-semibold px-2 py-0.5 rounded-md", 
                marketWidth >= 70 ? "bg-positive/10 text-positive" : 
                marketWidth >= 50 ? "bg-warning/10 text-warning" : "bg-negative/10 text-negative"
              )}>
                {marketWidth >= 70 ? "健康" : marketWidth >= 50 ? "分化" : "脆弱"}
              </span>
            </div>
            <p className="text-2xl font-mono font-semibold text-foreground">{marketWidth}%</p>
            <p className="text-xs text-foreground-muted mt-2">
              {marketWidth >= 70 ? "多数股票参与上涨，行情健康" : 
               marketWidth >= 50 ? "权重股领涨，多数股票涨不动" : 
               "市场极度分化，警惕回调"}
            </p>
          </div>

          {/* 趋势状态 */}
          <div className="bg-surface-elevated/30 border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-foreground-subtle">趋势状态</span>
              <span className={cn("text-xs font-semibold px-2 py-0.5 rounded-md",
                trendStatus === "uptrend" ? "bg-positive/10 text-positive" :
                trendStatus === "consolidation" ? "bg-warning/10 text-warning" : "bg-negative/10 text-negative"
              )}>
                {trendStatus === "uptrend" ? "上升趋势" : trendStatus === "consolidation" ? "震荡整理" : "下降趋势"}
              </span>
            </div>
            <p className="text-lg font-medium text-foreground">
              {trendStatus === "uptrend" ? "趋势跟随，不猜顶" : 
               trendStatus === "consolidation" ? "等待方向选择" : 
               "防御为主，控制仓位"}
            </p>
          </div>
        </div>
      </div>

      {/* 风险信号监控 */}
      <div>
        <h3 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-4">
          <AlertTriangle className="w-4 h-4 text-warning" />
          风险信号监控
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div className={cn("border rounded-lg p-4", topConstruction ? "bg-warning/5 border-warning/30" : "bg-surface-elevated/30 border-border")}>
            <div className="flex items-center gap-2 mb-2">
              <span className={cn("w-2 h-2 rounded-full", topConstruction ? "bg-warning" : "bg-positive")} />
              <span className="text-xs font-medium text-foreground-subtle">顶部构造</span>
            </div>
            <p className="text-sm text-foreground">{topConstruction ? "已形成，警惕回调" : "未观测到"}</p>
          </div>
          <div className={cn("border rounded-lg p-4", fomoGap ? "bg-warning/5 border-warning/30" : "bg-surface-elevated/30 border-border")}>
            <div className="flex items-center gap-2 mb-2">
              <span className={cn("w-2 h-2 rounded-full", fomoGap ? "bg-warning" : "bg-positive")} />
              <span className="text-xs font-medium text-foreground-subtle">FOMO 缺口</span>
            </div>
            <p className="text-sm text-foreground">{fomoGap ? "存在未回补缺口" : "无显著缺口"}</p>
          </div>
          <div className={cn("border rounded-lg p-4", liquidityAlert ? "bg-negative/5 border-negative/30" : "bg-surface-elevated/30 border-border")}>
            <div className="flex items-center gap-2 mb-2">
              <span className={cn("w-2 h-2 rounded-full", liquidityAlert ? "bg-negative" : "bg-positive")} />
              <span className="text-xs font-medium text-foreground-subtle">流动性警示</span>
            </div>
            <p className="text-sm text-foreground">{liquidityAlert ? "买卖盘失衡，警惕闪崩" : "流动性正常"}</p>
          </div>
        </div>
      </div>

      {/* 交易思维 */}
      <div className="bg-gradient-to-r from-primary/5 to-accent/5 border border-primary/20 rounded-lg p-5">
        <p className="text-sm text-foreground-muted italic leading-relaxed">
          &quot;在未見跡象之前，有理由繼續看漲。不是猜頂猜底，而是等待市場給出信號。&quot;
        </p>
        <p className="text-xs text-foreground-subtle mt-2">— 市场洞察</p>
      </div>
    </div>
  );
}
