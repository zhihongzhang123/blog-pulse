import type { Metadata } from "next";
import { ThemeProvider } from "@/lib/theme-provider";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { SearchModal } from "@/components/search-modal";
import { I18nProvider } from "@/i18n/provider";
import { getDictionary } from "@/i18n/dictionaries";
import "../globals.css";

export function generateStaticParams() {
  return [{ locale: "en" }, { locale: "zh" }];
}

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const dict = getDictionary(locale);
  const isZh = locale === "zh";

  return {
    title: {
      default: isZh ? "Pulse — 市场洞察与交易哲学" : "Pulse — Market Insights & Trading Philosophy",
      template: `%s | Pulse`,
    },
    description: isZh
      ? "交易哲学、市场分析与投资智慧的融合。数据驱动，逻辑导向，宇宙规律指引。"
      : "A fusion of trading philosophy, market analysis, and investment wisdom. Data-driven insights guided by cosmic rhythms and human nature.",
    metadataBase: new URL("https://blog.themarketpulse.uk"),
    openGraph: {
      type: "website",
      locale: isZh ? "zh_CN" : "en_US",
      url: "https://blog.themarketpulse.uk",
      title: isZh ? "Pulse — 市场洞察与交易哲学" : "Pulse — Market Insights & Trading Philosophy",
      description: isZh ? "交易哲学、市场分析与投资智慧的融合。" : "A fusion of trading philosophy, market analysis, and investment wisdom.",
      siteName: "Pulse",
    },
    twitter: {
      card: "summary_large_image",
      title: isZh ? "Pulse — 市场洞察与交易哲学" : "Pulse — Market Insights & Trading Philosophy",
      description: isZh ? "交易哲学、市场分析与投资智慧的融合。" : "A fusion of trading philosophy, market analysis, and investment wisdom.",
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
  const locale = (rawLocale === "en" || rawLocale === "zh") ? rawLocale : "en";
  const dict = getDictionary(locale);

  return (
    <html lang={locale} suppressHydrationWarning>
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
