export { en } from "./locales/en";
export { zh } from "./locales/zh";
export type { TranslationDict } from "./locales/en";

export const locales = ["en", "zh"] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = "en";

export function isValidLocale(locale: string): locale is Locale {
  return locales.includes(locale as Locale);
}
