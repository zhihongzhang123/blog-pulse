"use client";

import { useState, useEffect, useCallback } from "react";
import { Search, FileText, Calendar, BarChart3, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { useI18n } from "@/i18n/provider";

interface SearchResult {
  type: "article" | "briefing" | "market";
  title: string;
  description: string;
  href: string;
  date?: string;
}

const searchIndex: SearchResult[] = [
  {
    type: "article",
    title: "The Great Rotation: From AI to Real Economy",
    description: "Capital flows from mega-cap tech to industrials and energy",
    href: "/articles/great-rotation-ai-to-real-economy",
    date: "2026-05-02",
  },
  {
    type: "article",
    title: "大轮动：从 AI 到实体经济",
    description: "资本正从大型科技股流向工业、能源和基础设施",
    href: "/articles/great-rotation-ai-to-real-economy",
    date: "2026-05-02",
  },
  {
    type: "article",
    title: "The Art of Waiting",
    description: "Why patience is the most undervalued skill in trading",
    href: "/articles/art-of-waiting",
    date: "2026-03-21",
  },
  {
    type: "article",
    title: "等待的艺术",
    description: "耐心是交易中最被低估的技能",
    href: "/articles/art-of-waiting",
    date: "2026-03-21",
  },
  {
    type: "briefing",
    title: "Evening Briefing \u2014 May 2",
    description: "S&P 500 approaches 6,000, Fed holds rates",
    href: "/briefings/evening-20260502",
    date: "2026-05-02",
  },
  {
    type: "market",
    title: "S&P 500 Analysis",
    description: "Technical setup suggests consolidation phase",
    href: "/markets/sp500",
  },
];

const typeIcons = {
  article: FileText,
  briefing: Calendar,
  market: BarChart3,
};

export function SearchModal() {
  const { dict } = useI18n();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);

  const results = query.length >= 2
    ? searchIndex.filter(
        (r) =>
          r.title.toLowerCase().includes(query.toLowerCase()) ||
          r.description.toLowerCase().includes(query.toLowerCase())
      )
    : [];

  const handleOpen = useCallback(() => setOpen(true), []);
  const handleClose = useCallback(() => {
    setOpen(false);
    setQuery("");
    setSelectedIndex(0);
  }, []);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "/" && !open) {
        e.preventDefault();
        handleOpen();
      }
      if (e.key === "Escape" && open) {
        handleClose();
      }
      if (open) {
        if (e.key === "ArrowDown") {
          e.preventDefault();
          setSelectedIndex((i) => Math.min(i + 1, results.length - 1));
        }
        if (e.key === "ArrowUp") {
          e.preventDefault();
          setSelectedIndex((i) => Math.max(i - 1, 0));
        }
        if (e.key === "Enter" && results[selectedIndex]) {
          e.preventDefault();
          window.location.href = results[selectedIndex].href;
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, results, selectedIndex, handleOpen, handleClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-start justify-center pt-24 px-4"
      onClick={handleClose}
      role="dialog"
      aria-modal="true"
      aria-label="Search"
    >
      {/* Backdrop */}
      <div className="fixed inset-0 bg-background/80 backdrop-blur-sm" />

      {/* Modal */}
      <div
        className="relative w-full max-w-[36rem] bg-surface-elevated border border-border rounded-xl shadow-elevated overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Input */}
        <div className="flex items-center gap-3 px-4 border-b border-border">
          <Search className="w-5 h-5 text-foreground-muted flex-shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder={dict.search.placeholder}
            className="flex-1 py-4 bg-transparent text-foreground text-sm placeholder:text-foreground-subtle outline-none"
            autoFocus
          />
          <kbd className="hidden sm:inline-flex items-center px-1.5 py-0.5 text-xs text-foreground-subtle bg-surface rounded border border-border">
            ESC
          </kbd>
        </div>

        {/* Results */}
        <div className="max-h-80 overflow-y-auto">
          {query.length >= 2 && results.length === 0 && (
            <div className="px-4 py-8 text-center text-sm text-foreground-subtle">
              {dict.search.noResults} &quot;{query}&quot;
            </div>
          )}
          {query.length < 2 && (
            <div className="px-4 py-8 text-center text-sm text-foreground-subtle">
              {dict.search.minChars}
            </div>
          )}
          {results.map((result, i) => {
            const Icon = typeIcons[result.type];
            const typeLabel = dict.search[result.type as keyof typeof dict.search] as string;
            return (
              <a
                key={result.href + i}
                href={result.href}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 transition-colors duration-200",
                  i === selectedIndex
                    ? "bg-primary/10"
                    : "hover:bg-surface/50"
                )}
                onMouseEnter={() => setSelectedIndex(i)}
              >
                <Icon className="w-4 h-4 text-foreground-muted flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-foreground truncate">
                    {result.title}
                  </p>
                  <p className="text-xs text-foreground-subtle truncate">
                    {result.description}
                  </p>
                </div>
                <span className="text-xs text-foreground-subtle flex-shrink-0">
                  {typeLabel}
                </span>
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
}
