import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind classes with clsx
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Generate a localized path with locale prefix
 * Usage: href={localizedPath(locale, '/briefings')} → /zh/briefings or /en/briefings
 */
export function localizedPath(locale: string, path: string): string {
  // If path already has locale prefix, return as-is
  if (path.startsWith(`/${locale}/`) || path === `/${locale}`) {
    return path;
  }
  // Strip leading slash if present, then prepend with locale
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  return `/${locale}/${cleanPath}`;
}
