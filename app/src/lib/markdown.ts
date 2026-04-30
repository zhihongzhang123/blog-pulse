import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import { unified } from 'unified';

export async function renderMarkdown(md: string): Promise<string> {
  const result = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeSlug)
    .use(rehypeAutolinkHeadings, {
      behavior: 'append',
      properties: {
        class: 'heading-anchor',
      },
      content: () => ({
        type: 'element',
        tagName: 'span',
        properties: { className: ['anchor-symbol'] },
        children: [{ type: 'text', value: '#' }],
      }),
    })
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(md);

  return result.toString();
}

export function extractHeadings(md: string): { id: string; text: string; level: number }[] {
  return md
    .split('\n')
    .filter((line) => line.match(/^#{1,3}\s+/))
    .map((line) => {
      const match = line.match(/^(#{1,3})\s+(.+)$/);
      if (!match) return null;
      const level = match[1].length;
      const text = match[2].trim();
      const id = text
        .toLowerCase()
        .replace(/[^a-z0-9\u4e00-\u9fff]+/g, '-')
        .replace(/(^-|-$)/g, '');
      return { id, text, level };
    })
    .filter((h): h is { id: string; text: string; level: number } => h !== null);
}
