import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Calendar, Clock } from "lucide-react";
import fs from 'fs';
import path from 'path';
import "@/styles/article.css";
import { renderMarkdown, extractHeadings } from "@/lib/markdown";
import { getDictionary } from "@/i18n/dictionaries";
import type { Locale } from "@/i18n";

export const dynamicParams = false;

interface BriefingData {
  slug: string;
  title: string;
  date: string;
  time: string;
  type: 'morning' | 'evening';
  content: string;
  summary: string;
}

function getBriefingSlugs(): string[] {
  const briefingsDir = path.join(process.cwd(), '..', 'content', 'briefings');
  
  if (!fs.existsSync(briefingsDir)) {
    return [];
  }

  return fs.readdirSync(briefingsDir)
    .filter(f => f.endsWith('.md'))
    .map(f => f.replace('.md', ''));
}

export function generateStaticParams() {
  const slugs = getBriefingSlugs();
  return slugs.map((slug) => ({ slug }));
}

function readBriefingFile(slug: string): BriefingData | null {
  const filepath = path.join(process.cwd(), '..', 'content', 'briefings', `${slug}.md`);
  
  if (!fs.existsSync(filepath)) {
    return null;
  }

  const content = fs.readFileSync(filepath, 'utf-8');

  const parts = slug.split('-');
  if (parts.length < 2) return null;

  const type = parts[0] as 'morning' | 'evening';
  const dateStr = parts.slice(1).join('');
  const formattedDate = `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`;

  const titleMatch = content.match(/^(#+)\s+(.+)$/m);
  const title = titleMatch ? titleMatch[2].trim() : `${type === 'morning' ? '早报' : '晚报'}简报 — ${formattedDate}`;

  const timeMatch = content.match(/⏰\s*数据截点：(.+?)(?:\n|$)/);
  const time = timeMatch ? timeMatch[1].trim() : '';

  const summaryMatch = content.match(/##\s+核心主线\s*\n+(.+?)(?=\n##|\n---|$)/s);
  const summary = summaryMatch 
    ? summaryMatch[1].trim()
        .replace(/^>\s+/gm, '')
        .replace(/\*\*(.+?)\*\*/g, '$1')
        .replace(/\*(.+?)\*/g, '$1')
        .slice(0, 150) + '...'
    : '每日宏观交易简报';

  return {
    slug,
    title,
    date: formattedDate,
    time,
    type,
    content,
    summary,
  };
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const briefing = readBriefingFile(slug);
  
  if (!briefing) return { title: "Not Found" };

  return {
    title: `${briefing.title} | Pulse`,
    description: briefing.summary,
  };
}

export default async function BriefingPage({
  params,
}: {
  params: Promise<{ slug: string; locale: Locale }>;
}) {
  const { slug, locale } = await params;
  const briefing = readBriefingFile(slug);
  const dict = getDictionary(locale);
  
  if (!briefing) notFound();

  // Remove the first H1 from content since it's already displayed in the header
  const contentWithoutH1 = briefing.content.replace(/^#\s+.+$/m, '').replace(/^\n/, '');
  const htmlContent = await renderMarkdown(contentWithoutH1);
  const headings = extractHeadings(contentWithoutH1);

  return (
    <article className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      {/* Back button */}
      <Link
        href={`/${locale}/briefings`}
        className="inline-flex items-center gap-2 text-sm text-foreground-muted hover:text-primary transition-colors duration-200 mb-8"
      >
        <ArrowLeft className="w-4 h-4" />
        {dict.briefings.title}
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-[240px_1fr] gap-8 lg:gap-12">
        {/* Sidebar TOC */}
        <aside className="hidden lg:block">
          <nav className="sticky top-24 max-h-[calc(100vh-8rem)] overflow-y-auto" aria-label="Table of contents">
            <h2 className="text-xs font-semibold text-foreground-subtle uppercase tracking-wider mb-3 px-2">
              {locale === "zh" ? "目录" : "Contents"}
            </h2>
            <ul className="space-y-0.5">
              {headings.map((h) => (
                <li key={h.id}>
                  <a
                    href={`#${h.id}`}
                    className={`toc-link ${h.level === 2 ? 'toc-h2' : 'toc-h3'}`}
                  >
                    {h.text}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* Briefing content */}
        <div className="article-body max-w-[65ch] mx-auto lg:mx-0">
          <header className="mb-10 pb-6 border-b border-border">
            <div className="flex items-center gap-2 mb-4">
              <span
                className={`text-xs font-semibold px-2.5 py-1 rounded-md ${
                  briefing.type === "morning"
                    ? "bg-warning/10 text-warning"
                    : "bg-accent/10 text-accent"
                }`}
              >
                {briefing.type === "morning" ? dict.briefings.morning : dict.briefings.evening}
              </span>
              <span className="flex items-center gap-1.5 text-xs text-foreground-subtle">
                <Calendar className="w-3 h-3" />
                {briefing.date}
              </span>
              {briefing.time && (
                <span className="flex items-center gap-1.5 text-xs text-foreground-subtle">
                  <Clock className="w-3 h-3" />
                  {briefing.time}
                </span>
              )}
            </div>
            <h1 className="text-2xl sm:text-3xl font-semibold text-foreground tracking-tight mb-3 leading-snug">
              {briefing.title}
            </h1>
            <p className="text-sm text-foreground-muted leading-relaxed">
              {briefing.summary}
            </p>
          </header>

          <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
        </div>
      </div>

      {/* Mobile TOC */}
      <div className="lg:hidden mt-12 pt-6 border-t border-border">
        <h2 className="text-xs font-semibold text-foreground-subtle uppercase tracking-wider mb-4">
          {locale === "zh" ? "目录" : "Contents"}
        </h2>
        <div className="flex flex-wrap gap-2">
          {headings.map((h) => (
            <a
              key={h.id}
              href={`#${h.id}`}
              className={`text-xs px-3 py-1.5 rounded-full border border-border text-foreground-muted hover:text-primary hover:border-primary/30 transition-colors ${
                h.level === 3 ? 'opacity-70' : ''
              }`}
            >
              {h.text}
            </a>
          ))}
        </div>
      </div>
    </article>
  );
}
