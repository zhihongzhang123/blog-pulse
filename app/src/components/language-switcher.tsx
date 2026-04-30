"use client";

import { usePathname } from "next/navigation";
import { useI18n } from "@/i18n/provider";
import { Globe } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

export function LanguageSwitcher() {
  const { locale } = useI18n();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const switchLocale = (newLocale: string) => {
    const newPath = pathname.replace(/^\/(en|zh)/, `/${newLocale}`);
    window.location.href = newPath;
  };

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="p-1.5 rounded-md text-foreground-muted hover:text-foreground hover:bg-surface-elevated/50 transition-colors duration-200"
        aria-label="Switch language"
        aria-expanded={open}
      >
        <Globe className="w-4 h-4" />
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-32 bg-surface-elevated border border-border rounded-xl shadow-elevated overflow-hidden z-50">
          {[
            { code: "en", label: "English" },
            { code: "zh", label: "中文" },
          ].map((lang) => (
            <button
              key={lang.code}
              onClick={() => {
                switchLocale(lang.code);
                setOpen(false);
              }}
              className={cn(
                "w-full px-4 py-2.5 text-left text-sm flex items-center gap-3 transition-colors duration-200",
                locale === lang.code
                  ? "text-foreground bg-primary/10"
                  : "text-foreground-muted hover:text-foreground hover:bg-surface/50"
              )}
            >
              {lang.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
