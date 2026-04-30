"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTheme } from "@/lib/theme-provider";
import { useI18n } from "@/i18n/provider";
import { cn } from "@/lib/utils";
import {
  Sun,
  Moon,
  Monitor,
  Search,
  Menu,
  X,
} from "lucide-react";
import { useState, useEffect } from "react";
import { LanguageSwitcher } from "@/components/language-switcher";

export function Navbar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const { dict, locale } = useI18n();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [themeMenuOpen, setThemeMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 8);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  // Build nav items with locale prefix
  const navItems = [
    { label: dict.nav.home, href: `/${locale}` },
    { label: dict.nav.briefings, href: `/${locale}/briefings` },
    { label: dict.nav.articles, href: `/${locale}/articles` },
    { label: dict.nav.markets, href: `/${locale}/markets` },
    { label: dict.nav.about, href: `/${locale}/about` },
  ];

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
        scrolled
          ? "h-14 bg-background-secondary/80 backdrop-blur-xl border-b border-border shadow-frosted"
          : "h-16 bg-transparent"
      )}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-full flex items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className="text-lg font-medium tracking-tight text-foreground hover:text-primary transition-colors duration-200"
        >
          Pulse
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1" role="navigation" aria-label="Main navigation">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "px-3 py-1.5 text-sm rounded-md transition-colors duration-200",
                pathname === item.href
                  ? "text-foreground bg-surface-elevated"
                  : "text-foreground-muted hover:text-foreground hover:bg-surface-elevated/50"
              )}
              aria-current={pathname === item.href ? "page" : undefined}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        {/* Right actions */}
        <div className="flex items-center gap-1">
          {/* Search button */}
          <button
            className="hidden sm:flex items-center gap-2 px-3 py-1.5 text-sm text-foreground-muted bg-surface-elevated/50 rounded-md border border-border hover:border-border-hover transition-colors duration-200"
            aria-label="Search (press /)"
            onClick={() => {
              window.dispatchEvent(new KeyboardEvent("keydown", { key: "/" }));
            }}
          >
            <Search className="w-3.5 h-3.5" />
            <span className="text-foreground-subtle">/</span>
          </button>

          {/* Language Switcher */}
          <LanguageSwitcher />

          {/* Theme switcher */}
          <div className="relative">
            <button
              onClick={() => setThemeMenuOpen(!themeMenuOpen)}
              className="p-1.5 rounded-md text-foreground-muted hover:text-foreground hover:bg-surface-elevated/50 transition-colors duration-200"
              aria-label="Toggle theme"
              aria-expanded={themeMenuOpen}
            >
              {theme === "dark" && <Moon className="w-4 h-4" />}
              {theme === "light" && <Sun className="w-4 h-4" />}
              {theme === "system" && <Monitor className="w-4 h-4" />}
            </button>

            {themeMenuOpen && (
              <div className="absolute right-0 top-full mt-2 w-44 bg-surface-elevated border border-border rounded-xl shadow-elevated overflow-hidden">
                {(["light", "dark", "system"] as const).map((t) => (
                  <button
                    key={t}
                    onClick={() => {
                      setTheme(t);
                      setThemeMenuOpen(false);
                    }}
                    className={cn(
                      "w-full px-4 py-2.5 text-left text-sm flex items-center gap-3 transition-colors duration-200",
                      theme === t
                        ? "text-foreground bg-primary/10"
                        : "text-foreground-muted hover:text-foreground hover:bg-surface/50"
                    )}
                  >
                    {t === "light" && <Sun className="w-4 h-4" />}
                    {t === "dark" && <Moon className="w-4 h-4" />}
                    {t === "system" && <Monitor className="w-4 h-4" />}
                    <span className="capitalize">{t}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-1.5 rounded-md text-foreground-muted hover:text-foreground hover:bg-surface-elevated/50 transition-colors duration-200"
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile nav */}
      {mobileOpen && (
        <nav
          className="md:hidden bg-background-secondary/95 backdrop-blur-xl border-t border-border"
          role="navigation"
          aria-label="Mobile navigation"
        >
          <div className="px-4 py-3 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "block px-4 py-2.5 text-sm rounded-md transition-colors duration-200",
                  pathname === item.href
                    ? "text-foreground bg-surface-elevated"
                    : "text-foreground-muted hover:text-foreground hover:bg-surface-elevated/50"
                )}
                aria-current={pathname === item.href ? "page" : undefined}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </nav>
      )}
    </header>
  );
}
