import Link from "next/link";
import { ArrowUpRight, TrendingUp, TrendingDown, BookOpen, Clock, BarChart3, FileText, Brain, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { getDictionary } from "@/i18n/dictionaries";
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-static';

interface MarketData {
  indices: Record<string, { name: string; price: number; change_pct: number }>;
  extras: Record<string, { name: string; price: number; change_pct: number }>;
  commodities: Record<string, { name: string; price: number; change_pct: number }>;
  watchlist: Record<string, { name: string; price: number; change_pct: number }>;
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

const FALLBACK_INDICATORS = [
  { name: "S&P 500", value: "—", change: 0, positive: true },
  { name: "NASDAQ", value: "—", change: 0, positive: true },
  { name: "VIX", value: "—", change: 0, positive: true },
  { name: "US 10Y", value: "—", change: 0, positive: true },
];

interface BriefingInfo {
  title: string;
  summary: string;
  date: string;
  type: 'morning' | 'evening';
  href: string;
}

function getLatestBriefing(locale: string): BriefingInfo | null {
  const briefingsDir = path.join(process.cwd(), '..', 'content', 'briefings');
  
  if (!fs.existsSync(briefingsDir)) {
    return null;
  }

  const files = fs.readdirSync(briefingsDir)
    .filter(f => f.endsWith('.md'))
    .sort()
    .reverse();

  if (files.length === 0) return null;

  const latestFile = files[0];
  const slug = latestFile.replace('.md', '');
  const content = fs.readFileSync(
    path.join(briefingsDir, latestFile),
    'utf-8'
  );

  const titleMatch = content.match(/^#?\s*(.+)$/m);
  const title = titleMatch ? titleMatch[1].trim().replace(/^[\u{1F300}-\u{1F9FF}]\s*/u, '') : 'Latest Briefing';

  let summary = 'Daily macro trading briefing with market data and insights.';
  
  const summaryMatch = content.match(/##\s+核心主线\s*\n+(.+?)(?=\n##|\n---|$)/s);
  if (summaryMatch) {
    summary = summaryMatch[1].trim()
      .replace(/^>\s+/gm, '')
      .replace(/\*\*(.+?)\*\*/g, '$1')
      .replace(/\*(.+?)\*/g, '$1')
      .replace(/^#\s+.+$/gm, '')
      .replace(/\n+/g, ' ')
      .slice(0, 150) + '...';
  } else {
    const lines = content.split('\n');
    let inContent = false;
    for (const line of lines) {
      if (line.startsWith('# ')) {
        inContent = true;
        continue;
      }
      if (inContent && line.trim() && !line.startsWith('#') && !line.startsWith('---')) {
        summary = line.trim().slice(0, 150) + '...';
        break;
      }
    }
  }

  const parts = slug.split('-');
  const type = (parts[0] as 'morning' | 'evening') || 'evening';
  const dateStr = parts.slice(1).join('');
  const date = `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`;

  return {
    title,
    summary,
    date,
    type,
    href: `/${locale}/briefings/${slug}`,
  };
}

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const dict = getDictionary(locale);
  const latestBriefing = getLatestBriefing(locale);
  const marketData = getMarketData();
  const isZh = locale === "zh";

  // Build market indicators from live data
  const marketIndicators = marketData ? [
    {
      name: "S&P 500",
      value: marketData.indices?.SPY?.price.toLocaleString() ?? "—",
      change: marketData.indices?.SPY?.change_pct ?? 0,
      positive: (marketData.indices?.SPY?.change_pct ?? 0) >= 0,
    },
    {
      name: "NASDAQ",
      value: marketData.indices?.QQQ?.price.toLocaleString() ?? "—",
      change: marketData.indices?.QQQ?.change_pct ?? 0,
      positive: (marketData.indices?.QQQ?.change_pct ?? 0) >= 0,
    },
    {
      name: "VIX",
      value: marketData.extras?.VIX?.price.toFixed(2) ?? "—",
      change: marketData.extras?.VIX?.change_pct ?? 0,
      positive: (marketData.extras?.VIX?.change_pct ?? 0) <= 0, // VIX down is good
    },
    {
      name: "US 10Y",
      value: marketData.extras?.US10Y?.price ? `${(marketData.extras.US10Y.price * 100).toFixed(2)}%` : "—",
      change: marketData.extras?.US10Y?.change_pct ?? 0,
      positive: (marketData.extras?.US10Y?.change_pct ?? 0) <= 0, // Yield down is good for stocks
    },
  ] : FALLBACK_INDICATORS;

  // Build recent articles dynamically from content directory
  const articlesDir = path.join(process.cwd(), '..', 'content', 'articles');
  const recentArticlesData = fs.existsSync(articlesDir)
    ? fs.readdirSync(articlesDir)
        .filter(f => f.endsWith('.md'))
        .slice(0, 3)
        .map(filename => {
          const slug = filename.replace('.md', '');
          const content = fs.readFileSync(path.join(articlesDir, filename), 'utf-8');
          const titleMatch = content.match(/^#\s+(.+)$/m);
          const title = titleMatch ? titleMatch[1].trim() : slug.replace(/-/g, ' ');
          const dateMatch = content.match(/(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})/);
          const date = dateMatch ? dateMatch[1] : '';
          const categoryMatch = content.match(/分类[：:]\s*(.+)/);
          const category = categoryMatch ? categoryMatch[1].trim() : dict.articles.categories.analysis;
          const lines = content.split('\n').filter(l => l.trim() && !l.startsWith('#') && !l.startsWith('>') && !l.startsWith('---') && !l.startsWith('分类'));
          const excerpt = lines.slice(0, 2).join(' ').slice(0, 150);
          const iconMap: Record<string, React.ReactNode> = {
            'Analysis': <BarChart3 className="w-4 h-4" />,
            'analysis': <BarChart3 className="w-4 h-4" />,
            'Philosophy': <Brain className="w-4 h-4" />,
            'philosophy': <Brain className="w-4 h-4" />,
          };
          return {
            title,
            excerpt,
            date,
            category,
            icon: iconMap[category] || <FileText className="w-4 h-4" />,
            href: `/${locale}/articles/${slug}`,
          };
        })
    : [];

  const recentArticles = recentArticlesData.length > 0 ? recentArticlesData : [
    { title: "大轮动：从 AI 到实体经济", excerpt: "资本正从大型科技股流向工业、能源和基础设施。", date: "2026-05-02", category: dict.articles.categories.analysis, icon: <BarChart3 className="w-4 h-4" />, href: `/${locale}/articles/great-rotation-ai-to-real-economy` },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      {/* Hero */}
      <section className="mb-12 sm:mb-16">
        <h1 className="text-3xl sm:text-4xl font-semibold text-foreground tracking-tight mb-3">
          {dict.home.title}
        </h1>
        <p className="text-lg text-foreground-muted max-w-[42rem] leading-relaxed">
          {dict.home.subtitle}
        </p>
      </section>

      {/* Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 sm:gap-6">
        {/* Market Indicators */}
        <div className="md:col-span-8 bg-surface border border-border rounded-xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-sm font-semibold text-foreground flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-primary" />
              {dict.home.marketIndicators}
            </h2>
            <Link
              href={`/${locale}/markets`}
              className="text-xs text-foreground-muted hover:text-primary transition-colors duration-200 flex items-center gap-1"
            >
              {dict.home.viewAll} <ArrowUpRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-5">
            {marketIndicators.map((indicator) => (
              <div key={indicator.name} className="space-y-1.5">
                <p className="text-xs text-foreground-subtle font-medium">{indicator.name}</p>
                <p className="text-xl font-mono font-semibold text-foreground tracking-tight">
                  {indicator.value}
                </p>
                <p
                  className={cn(
                    "text-xs font-medium flex items-center gap-1",
                    indicator.positive ? "text-positive" : "text-negative"
                  )}
                >
                  {indicator.positive ? (
                    <TrendingUp className="w-3 h-3" />
                  ) : (
                    <TrendingDown className="w-3 h-3" />
                  )}
                  {indicator.change > 0 ? "+" : ""}
                  {indicator.change.toFixed(2)}%
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Latest Briefing */}
        <div className="md:col-span-4 bg-surface border border-border rounded-xl p-6 flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <Clock className="w-4 h-4 text-warning" />
            <h2 className="text-sm font-semibold text-foreground">{dict.home.latestBriefing}</h2>
          </div>
          {latestBriefing ? (
            <>
              <Link href={latestBriefing.href} className="flex-1 group">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-md ${
                    latestBriefing.type === "morning"
                      ? "bg-warning/10 text-warning"
                      : "bg-accent/10 text-accent"
                  }`}>
                    {latestBriefing.type === "morning" ? dict.home.morning : dict.home.evening}
                  </span>
                  <time className="text-xs text-foreground-subtle">
                    {latestBriefing.date}
                  </time>
                </div>
                <h3 className="text-base font-medium text-foreground group-hover:text-primary transition-colors duration-200 mb-2 leading-snug">
                  {latestBriefing.title}
                </h3>
                <p className="text-sm text-foreground-muted leading-relaxed line-clamp-3">
                  {latestBriefing.summary}
                </p>
              </Link>
              <Link
                href={`/${locale}/briefings`}
                className="mt-4 text-xs text-foreground-muted hover:text-primary transition-colors duration-200 flex items-center gap-1"
              >
                {dict.home.allBriefings} <ChevronRight className="w-3 h-3" />
              </Link>
            </>
          ) : (
            <p className="text-sm text-foreground-muted">{dict.home.noBriefings}</p>
          )}
        </div>

        {/* Recent Articles */}
        <div className="md:col-span-12 bg-surface border border-border rounded-xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-sm font-semibold text-foreground flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-primary" />
              {dict.home.recentArticles}
            </h2>
            <Link
              href={`/${locale}/articles`}
              className="text-xs text-foreground-muted hover:text-primary transition-colors duration-200 flex items-center gap-1"
            >
              {dict.home.allArticles} <ArrowUpRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {recentArticles.map((article) => (
              <Link
                key={article.href}
                href={article.href}
                className="group flex flex-col bg-surface-elevated/30 border border-border rounded-lg p-5 hover:border-border-hover hover:bg-surface-elevated/50 transition-all duration-200"
              >
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-primary">{article.icon}</span>
                  <span className="text-xs font-semibold text-primary">{article.category}</span>
                </div>
                <h3 className="text-base font-medium text-foreground group-hover:text-primary transition-colors duration-200 mb-2 line-clamp-2 leading-snug">
                  {article.title}
                </h3>
                <p className="text-sm text-foreground-muted leading-relaxed line-clamp-3 flex-1">
                  {article.excerpt}
                </p>
                <time className="text-xs text-foreground-subtle mt-3">
                  {article.date}
                </time>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Philosophy Quote */}
      <section className="mt-16 sm:mt-20 text-center">
        <blockquote className="text-lg sm:text-xl text-foreground-muted italic leading-relaxed max-w-[42rem] mx-auto">
          {dict.home.quote}
        </blockquote>
        <p className="mt-3 text-sm text-foreground-subtle">{dict.home.quoteAuthor}</p>
      </section>
    </div>
  );
}
