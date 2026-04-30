import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { getDictionary } from "@/i18n/dictionaries";

export default async function AboutPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const dict = getDictionary(locale);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <div className="max-w-[65ch] mx-auto">
        <header className="mb-10">
          <h1 className="text-3xl font-medium text-foreground tracking-tight mb-3">
            {dict.about.title}
          </h1>
          <p className="text-lg text-foreground-muted leading-relaxed">
            {dict.about.subtitle}
          </p>
        </header>

        <div className="space-y-6 text-base text-foreground-muted leading-relaxed">
          <p>
            {dict.about.intro}
          </p>

          <h2 className="text-xl font-medium text-foreground mt-10 mb-4">
            {dict.about.philosophy}
          </h2>
          <p>
            {dict.about.philosophyIntro}
          </p>

          <ul className="space-y-3 pl-6 list-disc marker:text-primary">
            <li>
              <strong className="text-foreground">Warren Buffett</strong> — {dict.about.buffet}
            </li>
            <li>
              <strong className="text-foreground">Charlie Munger</strong> — {dict.about.munger}
            </li>
            <li>
              <strong className="text-foreground">Jesse Livermore</strong> — {dict.about.livermore}
            </li>
            <li>
              <strong className="text-foreground">Ray Dalio</strong> — {dict.about.dalio}
            </li>
            <li>
              <strong className="text-foreground">Cathie Wood</strong> — {dict.about.wood}
            </li>
          </ul>

          <h2 className="text-xl font-medium text-foreground mt-10 mb-4">
            {dict.about.whatYoullFind}
          </h2>
          <ul className="space-y-3 pl-6 list-disc marker:text-primary">
            <li>
              <strong className="text-foreground">{dict.about.dailyBriefings}</strong> — {dict.about.dailyBriefingsDesc}
            </li>
            <li>
              <strong className="text-foreground">{dict.about.deepArticles}</strong> — {dict.about.deepArticlesDesc}
            </li>
            <li>
              <strong className="text-foreground">{dict.about.marketData}</strong> — {dict.about.marketDataDesc}
            </li>
          </ul>

          <blockquote className="border-l-2 border-primary/30 pl-4 py-3 my-8 text-foreground italic">
            &quot;The four most dangerous words in investing are: &apos;it&apos;s
            different this time.&quot;
            <footer className="mt-1 not-italic text-foreground-subtle text-sm">
              — Sir John Templeton
            </footer>
          </blockquote>

          <h2 className="text-xl font-medium text-foreground mt-10 mb-4">
            {dict.about.connect}
          </h2>
          <p>
            {dict.about.connectDesc}{" "}
            <a
              href="https://github.com/zhihongzhang123/blog-pulse"
              className="text-primary hover:underline"
            >
              GitHub
            </a>
            .
          </p>

          <div className="mt-10 pt-6 border-t border-border">
            <Link
              href={`/${locale}`}
              className="text-sm text-primary hover:underline flex items-center gap-1"
            >
              {dict.about.backToHome} <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
