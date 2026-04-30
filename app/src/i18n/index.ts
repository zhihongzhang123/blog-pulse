export { zh } from "./locales/zh";
export type { TranslationDict } from "./locales/en";

export const locales = ["zh"] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = "zh";

export function isValidLocale(locale: string): locale is Locale {
  return locales.includes(locale as Locale);
}
