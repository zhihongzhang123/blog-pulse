"use client";

import { createContext, useContext, useMemo } from "react";
import type { TranslationDict } from "./locales/en";

interface I18nContextValue {
  dict: TranslationDict;
  locale: string;
}

const I18nContext = createContext<I18nContextValue | null>(null);

export function I18nProvider({
  children,
  dict,
  locale,
}: {
  children: React.ReactNode;
  dict: TranslationDict;
  locale: string;
}) {
  const value = useMemo(
    () => ({ dict, locale }),
    [dict, locale]
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error("useI18n must be used within I18nProvider");
  return ctx;
}

export function useTranslations() {
  const { dict } = useI18n();

  return function t(path: string): string {
    const parts = path.split(".");
    let current: unknown = dict;
    for (const part of parts) {
      if (current && typeof current === "object" && part in current) {
        current = (current as Record<string, unknown>)[part];
      } else {
        return path;
      }
    }
    return typeof current === "string" ? current : path;
  };
}
