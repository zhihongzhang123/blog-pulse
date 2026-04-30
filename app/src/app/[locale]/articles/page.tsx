import Link from "next/link";
import { ArrowUpRight, Clock } from "lucide-react";
import { getDictionary } from "@/i18n/dictionaries";
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-static';

function getArticlesDir(): string {
  return path.join(process.cwd(), '..', 'content', 'articles');
}

interface ArticleInfo {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  category: string;
  readTime: string;
}

function getArticles(): ArticleInfo[] {
  const dir = getArticlesDir();
  if (!fs.existsSync(dir)) return [];

  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .map(filename => {
      const slug = filename.replace('.md', '');
      const content = fs.readFileSync(path.join(dir, filename), 'utf-8');

      const titleMatch = content.match(/^#\s+(.+)$/m);
      const title = titleMatch ? titleMatch[1].trim() : slug.replace(/-/g, ' ');

      const dateMatch = content.match(/(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})/);
      const date = dateMatch ? dateMatch[1] : '';

      const categoryMatch = content.match(/分类[：:]\s*(.+)/);
      const category = categoryMatch ? categoryMatch[1].trim() : 'Analysis';

      // First non-heading paragraph as excerpt
      const lines = content.split('\n').filter(l => l.trim() && !l.startsWith('#') && !l.startsWith('>') && !l.startsWith('---') && !l.startsWith('分类'));
      const excerpt = lines.slice(0, 2).join(' ').slice(0, 160);

      // Estimate read time (~200 words/min)
      const wordCount = content.split(/\s+/).length;
      const readTime = `${Math.max(1, Math.ceil(wordCount / 200))} min`;

      return { slug, title, excerpt, date, category, readTime };
    })
    .sort((a, b) => b.date.localeCompare(a.date));
}

export default async function ArticlesPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const dict = getDictionary(locale);
  const articles = getArticles();

  if (articles.length === 0) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
        <header className="mb-10">
          <h1 className="text-3xl font-medium text-foreground tracking-tight mb-3">
            {dict.articles.title}
          </h1>
          <p className="text-lg text-foreground-muted">
            {dict.articles.subtitle}
          </p>
        </header>
        <div className="text-center py-20 text-foreground-muted">
          No articles yet.
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <header className="mb-10">
        <h1 className="text-3xl font-medium text-foreground tracking-tight mb-3">
          {dict.articles.title}
        </h1>
        <p className="text-lg text-foreground-muted">
          {dict.articles.subtitle}
        </p>
      </header>

      <div className="space-y-6">
        {articles.map((article) => (
          <Link
            key={article.slug}
            href={`/${locale}/articles/${article.slug}`}
            className="group block bg-surface border border-border rounded-xl p-6 hover:border-border-hover transition-colors duration-200"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <span className="text-xs text-primary mb-2 block">
                  {article.category}
                </span>
                <h2 className="text-lg font-medium text-foreground group-hover:text-primary transition-colors duration-200 mb-2">
                  {article.title}
                </h2>
                <p className="text-sm text-foreground-muted leading-relaxed line-clamp-2">
                  {article.excerpt}
                </p>
                <div className="flex items-center gap-3 mt-3">
                  {article.date && (
                    <time className="text-xs text-foreground-subtle">
                      {article.date}
                    </time>
                  )}
                  <span className="text-xs text-foreground-subtle flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {article.readTime}
                  </span>
                </div>
              </div>
              <ArrowUpRight className="w-5 h-5 text-foreground-subtle group-hover:text-primary transition-colors duration-200 flex-shrink-0 mt-1" />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
