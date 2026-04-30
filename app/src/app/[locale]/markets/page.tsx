import { TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { getDictionary } from "@/i18n/dictionaries";
import { SP500Chart } from "@/components/sp500-chart";
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-static';

interface MarketData {
  indices: Record<string, { name: string; price: number; change_pct: number }>;
  extras: Record<string, { name: string; price: number; change_pct: number }>;
  commodities: Record<string, { name: string; price: number; change_pct: number }>;
  watchlist: Record<string, { name: string; price: number; change_pct: number }>;
  chart_data?: Array<{ date: string; value: number }>;
}

function getMarketData(): MarketData | null {
  const dataPath = path.join(process.cwd(), '..', 'content', 'market-data.json');
  if (!fs.existsSync(dataPath)) return null;
  try {
    return JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
  } catch {
    return null;
  }
}

function renderPrice(value: number | undefined, key?: string): string {
  if (value === undefined) return "—";
  if (key === "US10Y") return `${(value * 100).toFixed(2)}%`;
  if (key === "CL" || key === "GC" || key === "SI") return `$${value.toLocaleString()}`;
  return value.toLocaleString();
}

export default async function MarketsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const dict = getDictionary(locale);
  const marketData = getMarketData();

  const indicesList = marketData ? Object.entries(marketData.indices || {}).map(([key, v]) => ({
    key,
    name: v.name,
    value: renderPrice(v.price, key),
    change: v.change_pct,
  })) : [];

  const commoditiesList = marketData ? Object.entries(marketData.commodities || {}).map(([key, v]) => ({
    key,
    name: v.name,
    value: renderPrice(v.price, key),
    change: v.change_pct,
  })) : [];

  const spyData = marketData?.indices?.SPY;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <header className="mb-10">
        <h1 className="text-3xl font-medium text-foreground tracking-tight mb-3">
          {dict.markets.title}
        </h1>
        <p className="text-lg text-foreground-muted">
          {dict.markets.subtitle}
        </p>
      </header>

      {/* S&P 500 Chart */}
      <section className="bg-surface border border-border rounded-xl p-6 mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-medium text-foreground">S&P 500</h2>
          {spyData && (
            <div className="flex items-center gap-2">
              <span className="text-2xl font-medium text-foreground">{spyData.price.toLocaleString()}</span>
              <span className={cn("text-sm font-medium flex items-center gap-1", spyData.change_pct >= 0 ? "text-positive" : "text-negative")}>
                {spyData.change_pct >= 0 ? (
                  <TrendingUp className="w-4 h-4" />
                ) : (
                  <TrendingDown className="w-4 h-4" />
                )}
                {spyData.change_pct > 0 ? "+" : ""}{spyData.change_pct.toFixed(2)}%
              </span>
            </div>
          )}
        </div>
        <SP500Chart data={marketData?.chart_data} />
      </section>

      {/* Indices Grid */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {indicesList.map((idx) => (
          <div key={idx.key} className="bg-surface border border-border rounded-xl p-5">
            <p className="text-xs text-foreground-subtle mb-1">{idx.name}</p>
            <p className="text-xl font-medium text-foreground tracking-tight mb-1">{idx.value}</p>
            <p className={cn("text-sm font-medium flex items-center gap-1", idx.change >= 0 ? "text-positive" : "text-negative")}>
              {idx.change >= 0 ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
              {idx.change > 0 ? "+" : ""}{idx.change.toFixed(2)}%
            </p>
          </div>
        ))}
      </section>

      {/* Commodities */}
      <section className="bg-surface border border-border rounded-xl p-6">
        <h2 className="text-lg font-medium text-foreground mb-5">{dict.markets.commodities}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {commoditiesList.map((c) => (
            <div key={c.key} className="space-y-1">
              <p className="text-xs text-foreground-subtle">{c.name}</p>
              <p className="text-lg font-medium text-foreground">{c.value}</p>
              <p className={cn("text-sm font-medium", c.change >= 0 ? "text-positive" : "text-negative")}>
                {c.change > 0 ? "+" : ""}{c.change.toFixed(2)}%
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
