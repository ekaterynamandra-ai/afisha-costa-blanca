// Helpers around the single `articles` collection.

import { getCollection, type CollectionEntry } from 'astro:content';
import { type Locale, type NavCurrent, localeFromId, sectionPath, sectionSlug } from '../i18n';
import type { Section } from '../content.config';

export type ArticleWithMeta = CollectionEntry<'articles'> & {
  _meta: { locale: Locale; section: Section; slug: string };
};

/** All published articles in a given locale, optionally filtered by section. */
export async function getArticles(locale: Locale, section?: Section): Promise<ArticleWithMeta[]> {
  const entries = await getCollection('articles', ({ data }) => !data.draft);
  return entries
    .map((e) => ({ ...e, _meta: localeFromId(e.id) }))
    .filter((e) => e._meta.locale === locale)
    .filter((e) => (section ? e._meta.section === section : true));
}

/** Canonical URL for a given article. */
export function articleUrl(locale: Locale, section: Section, slug: string): string {
  return `${sectionPath[locale][section]}${slug}/`;
}

/** Section listing URL (e.g. /pereezd/ or /en/moving/). */
export function sectionUrl(locale: Locale, section: Section): string {
  return sectionPath[locale][section];
}

/** Find the same article in the other locale by matching slug. */
export function altArticleUrl(
  allEntries: ArticleWithMeta[],
  altLocale: Locale,
  section: Section,
  slug: string,
): string {
  const match = allEntries.find(
    (e) => e._meta.locale === altLocale && e._meta.section === section && e._meta.slug === slug,
  );
  return match ? articleUrl(altLocale, section, slug) : sectionPath[altLocale][section];
}
