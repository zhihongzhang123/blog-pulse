"use client";

import Link from "next/link";
import { useI18n } from "@/i18n/provider";

export function Footer() {
  const { dict, locale } = useI18n();

  return (
    <footer className="border-t border-border bg-background-secondary/50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <h3 className="text-lg font-medium text-foreground mb-3">Pulse</h3>
            <p className="text-sm text-foreground-muted leading-relaxed whitespace-pre-line">
              {dict.footer.description}
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-sm font-medium text-foreground mb-3">{dict.footer.navigate}</h4>
            <ul className="space-y-2">
              <li>
                <Link
                  href={`/${locale}/briefings`}
                  className="text-sm text-foreground-muted hover:text-foreground transition-colors duration-200"
                >
                  {dict.nav.briefings}
                </Link>
              </li>
              <li>
                <Link
                  href={`/${locale}/articles`}
                  className="text-sm text-foreground-muted hover:text-foreground transition-colors duration-200"
                >
                  {dict.nav.articles}
                </Link>
              </li>
              <li>
                <Link
                  href={`/${locale}/markets`}
                  className="text-sm text-foreground-muted hover:text-foreground transition-colors duration-200"
                >
                  {dict.nav.markets}
                </Link>
              </li>
              <li>
                <Link
                  href={`/${locale}/about`}
                  className="text-sm text-foreground-muted hover:text-foreground transition-colors duration-200"
                >
                  {dict.nav.about}
                </Link>
              </li>
            </ul>
          </div>

          {/* Philosophy */}
          <div>
            <h4 className="text-sm font-medium text-foreground mb-3">{dict.footer.philosophy}</h4>
            <blockquote className="text-sm text-foreground-subtle italic leading-relaxed">
              {dict.footer.quote}
              <footer className="mt-1 not-italic text-foreground-subtle">
                {dict.footer.quoteAuthor}
              </footer>
            </blockquote>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-border flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-xs text-foreground-subtle">
            &copy; {new Date().getFullYear()} Pulse. {dict.footer.rights}
          </p>
          <p className="text-xs text-foreground-subtle">
            {dict.footer.tagline}
          </p>
        </div>
      </div>
    </footer>
  );
}
