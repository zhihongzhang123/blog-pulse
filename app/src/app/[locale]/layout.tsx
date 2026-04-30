import type { Metadata } from "next";
import { ThemeProvider } from "@/lib/theme-provider";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { SearchModal } from "@/components/search-modal";
import { I18nProvider } from "@/i18n/provider";
import { getDictionary } from "@/i18n/dictionaries";
import "../globals.css";

export function generateStaticParams() {
  return [{ locale: "zh" }];
}

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const dict = getDictionary(locale);

  return {
    title: {
      default: "Pulse — 市场洞察与交易哲学",
      template: `%s | Pulse`,
    },
    description: "交易哲学、市场分析与投资智慧的融合。数据驱动，逻辑导向，宇宙规律指引。",
    metadataBase: new URL("https://blog.themarketpulse.uk"),
    openGraph: {
      type: "website",
      locale: "zh_CN",
      url: "https://blog.themarketpulse.uk",
      title: "Pulse — 市场洞察与交易哲学",
      description: "交易哲学、市场分析与投资智慧的融合。",
      siteName: "Pulse",
    },
    twitter: {
      card: "summary_large_image",
      title: "Pulse — 市场洞察与交易哲学",
      description: "交易哲学、市场分析与投资智慧的融合。",
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}

export default async function RootLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale: rawLocale } = await params;
  const locale = "zh";
  const dict = getDictionary(locale);

  return (
    <html lang={locale} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                document.querySelectorAll('[data-darkreader-inline-stroke]').forEach(function(el) {
                  el.removeAttribute('data-darkreader-inline-stroke');
                  el.style.removeProperty('--darkreader-inline-stroke');
                });
              } catch(e) {}
            })();
          `
        }} />
      </head>
      <body className="min-h-screen bg-background text-foreground antialiased" suppressHydrationWarning>
        <I18nProvider dict={dict} locale={locale}>
          <ThemeProvider>
            <div className="flex flex-col min-h-screen">
              <Navbar />
              <main className="flex-1 pt-16">{children}</main>
              <Footer />
            </div>
            <SearchModal />
          </ThemeProvider>
        </I18nProvider>
      </body>
    </html>
  );
}
