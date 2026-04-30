import fs from 'fs';
import path from 'path';
import Link from 'next/link';
import { Calendar, ArrowUpRight, Clock, FileText } from 'lucide-react';
import { getDictionary } from '@/i18n/dictionaries';
import type { Locale } from '@/i18n';

export const dynamic = 'force-static';

interface Briefing {
  id: string;
  title: string;
  date: string;
  time: string;
  type: 'morning' | 'evening';
  summary: string;
  slug: string;
}

function parseBriefingFile(filename: string): Briefing | null {
  const slug = filename.replace('.md', '');
  const content = fs.readFileSync(
    path.join(process.cwd(), '..', 'content', 'briefings', filename),
    'utf-8'
  );

  const parts = slug.split('-');
  if (parts.length < 2) return null;

  const type = parts[0] as 'morning' | 'evening';
  const dateStr = parts.slice(1).join('');
  
  const formattedDate = `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`;

  const titleMatch = content.match(/^#?\s*(.+)$/m);
  const title = titleMatch ? titleMatch[1].trim().replace(/^[\u{1F300}-\u{1F9FF}]\s*/u, '') : `${type === 'morning' ? '早报' : '晚报'}简报 — ${formattedDate}`;

  const timeMatch = content.match(/⏰\s*数据截点：(.+?)(?:\n|$)/);
  const time = timeMatch ? timeMatch[1].trim() : '';

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

  return {
    id: slug,
    title,
    date: formattedDate,
    time,
    type,
    summary,
    slug,
  };
}

function getBriefings(): Briefing[] {
  const briefingsDir = path.join(process.cwd(), '..', 'content', 'briefings');
  
  if (!fs.existsSync(briefingsDir)) {
    return [];
  }

  const files = fs.readdirSync(briefingsDir)
    .filter(f => f.endsWith('.md'))
    .sort()
    .reverse();

  return files
    .map(parseBriefingFile)
    .filter((b): b is Briefing => b !== null);
}

export default async function BriefingsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const dict = getDictionary(locale);
  const briefings = getBriefings();

  if (briefings.length === 0) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
        <header className="mb-10">
          <h1 className="text-3xl font-semibold text-foreground tracking-tight mb-3">
            {dict.briefings.title}
          </h1>
          <p className="text-lg text-foreground-muted">
            {dict.briefings.subtitle}
          </p>
        </header>

        <div className="text-center py-20">
          <FileText className="w-12 h-12 text-foreground-subtle mx-auto mb-4" />
          <p className="text-foreground-muted">{dict.briefings.noBriefings}</p>
          <p className="text-sm text-foreground-subtle mt-2">
            {dict.briefings.noBriefingsSub}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <header className="mb-10">
        <h1 className="text-3xl font-semibold text-foreground tracking-tight mb-3">
          {dict.briefings.title}
        </h1>
        <p className="text-lg text-foreground-muted">
          {dict.briefings.subtitle}
        </p>
      </header>

      <div className="space-y-4">
        {briefings.map((b) => (
          <Link
            key={b.id}
            href={`/${locale}/briefings/${b.slug}`}
            className="group flex items-start gap-4 bg-surface border border-border rounded-xl p-5 hover:border-border-hover hover:bg-surface-elevated/30 transition-all duration-200"
          >
            <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-surface-elevated flex items-center justify-center">
              <Calendar className="w-5 h-5 text-foreground-muted" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                <span
                  className={`text-xs font-semibold px-2 py-0.5 rounded-md ${
                    b.type === "morning"
                      ? "bg-warning/10 text-warning"
                      : "bg-accent/10 text-accent"
                  }`}
                >
                  {b.type === "morning" ? dict.briefings.morning : dict.briefings.evening}
                </span>
                <time className="text-xs text-foreground-subtle">
                  {b.date}
                </time>
                {b.time && (
                  <span className="flex items-center gap-1 text-xs text-foreground-subtle">
                    <Clock className="w-3 h-3" />
                    {b.time}
                  </span>
                )}
              </div>
              <h2 className="text-base font-medium text-foreground group-hover:text-primary transition-colors duration-200 mb-1.5 leading-snug">
                {b.title}
              </h2>
              <p className="text-sm text-foreground-muted leading-relaxed line-clamp-2">
                {b.summary}
              </p>
            </div>
            <div className="flex-shrink-0 mt-1">
              <ArrowUpRight className="w-4 h-4 text-foreground-subtle group-hover:text-primary transition-colors duration-200" />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
