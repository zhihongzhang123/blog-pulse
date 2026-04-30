import type { Locale } from "./index";
import { en } from "./locales/en";
import { zh } from "./locales/zh";
import type { TranslationDict } from "./locales/en";

const dictionaries: Record<string, TranslationDict> = {
  en,
  zh,
};

export function getDictionary(locale: string): TranslationDict {
  return dictionaries[locale] ?? dictionaries.en;
}
