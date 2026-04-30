import type { Metadata } from "next";
import { notFound } from "next/navigation";
import "@/styles/article.css";
import fs from 'fs';
import path from 'path';
import { renderMarkdown, extractHeadings } from "@/lib/markdown";

export const dynamicParams = false;

function getArticlesDir(): string {
  return path.join(process.cwd(), '..', 'content', 'articles');
}

function getArticleSlugs(): string[] {
  const dir = getArticlesDir();
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .map(f => f.replace('.md', ''));
}

export function generateStaticParams() {
  return getArticleSlugs().map((slug) => ({ slug }));
}

interface ArticleData {
  slug: string;
  title: string;
  date: string;
  category: string;
  content: string;
  summary: string;
}

function readArticleFile(slug: string): ArticleData | null {
  const filepath = path.join(getArticlesDir(), `${slug}.md`);
  if (!fs.existsSync(filepath)) return null;

  const content = fs.readFileSync(filepath, 'utf-8');

  // Extract title from first H1
  const titleMatch = content.match(/^#\s+(.+)$/m);
  const title = titleMatch ? titleMatch[1].trim() : slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

  // Extract date from content or filename
  const dateMatch = content.match(/(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})/);
  const date = dateMatch ? dateMatch[1] : '';

  // Extract category from tags or default
  const categoryMatch = content.match(/分类[：:]\s*(.+)/);
  const category = categoryMatch ? categoryMatch[1].trim() : 'Analysis';

  // Extract summary (first paragraph after title)
  const lines = content.split('\n').filter(l => l.trim() && !l.startsWith('#') && !l.startsWith('>') && !l.startsWith('---'));
  const summary = lines.slice(0, 3).join(' ').slice(0, 160);

  return { slug, title, date, category, content, summary };
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const article = readArticleFile(slug);
  if (!article) return { title: "Not Found" };

  return {
    title: `${article.title} | Pulse`,
    description: article.summary,
  };
}

export default async function ArticlePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const article = readArticleFile(slug);
  if (!article) notFound();

  // Remove the first H1 from content since it's already displayed in the header
  const contentWithoutH1 = article.content.replace(/^#\s+.+$/m, '').replace(/^\n/, '');
  const htmlContent = await renderMarkdown(contentWithoutH1);
  const headings = extractHeadings(contentWithoutH1);

  return (
    <article className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <div className="grid grid-cols-1 lg:grid-cols-[200px_1fr] gap-8 lg:gap-12">
        {/* Sidebar TOC */}
        <aside className="hidden lg:block">
          <nav className="sticky top-24" aria-label="Table of contents">
            <h2 className="text-xs font-medium text-foreground-subtle uppercase tracking-wider mb-3">
              Contents
            </h2>
            <ul className="space-y-1">
              {headings.map((h) => (
                <li key={h.id}>
                  <a href={`#${h.id}`} className="toc-link">
                    {h.text}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* Article content */}
        <div className="article-body max-w-[65ch] mx-auto lg:mx-0">
          <header className="mb-8">
            <span className="text-xs text-primary mb-2 block">{article.category}</span>
            <h1 className="text-3xl sm:text-4xl font-medium text-foreground tracking-tight mb-3">
              {article.title}
            </h1>
            {article.date && (
              <time className="text-sm text-foreground-subtle">{article.date}</time>
            )}
          </header>
          <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
        </div>
      </div>
    </article>
  );
}
