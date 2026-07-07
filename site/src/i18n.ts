// Centralised i18n helpers — single source of truth for nav labels,
// URL prefixes and locale detection.

export const LOCALES = ['ru', 'en'] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = 'ru';

import type { Section } from './content.config';

export const ui = {
  ru: {
    'nav.home': 'Домой',
    'nav.pereezd': 'Переезд',
    'nav.zhizn': 'Жизнь',
    'nav.biznes': 'Онлайн-работа',
    'nav.ai': 'AI в работе и жизни',
    'nav.about': 'Про меня',

    'home.hero.eyebrow': 'Kate in Spain',
    'home.hero.title': 'Жить у моря, работать удалённо',
    'home.hero.lead': 'Гайды, инструменты и опыт для тех, кто переезжает в Испанию или уже здесь живёт. В порядке, в котором это нужно: сначала добраться, потом жить, потом — работать и расти.',
    'home.cta.primary': 'С чего начать',
    'home.cta.telegram': 'Телеграм-канал',

    'home.sections.title': 'Четыре опоры',
    'home.sections.sub': 'В том порядке, в котором это происходит на самом деле: сначала переезд и жизнь, потом — заработать и расти.',

    'home.about.title': 'Кто это всё пишет',
    'home.about.sub': 'Катя — живёт в Испании, ведёт телеграм-сообщество и параллельно с мужем строит AI Studio. Две темы сведены в одно место, потому что я живу обеими.',
    'home.about.cta': 'Подробнее',

    'home.telegram.title': 'Каждую неделю — в Telegram',
    'home.telegram.sub': 'Сайт — это база знаний. Свежие подборки, события и короткие наблюдения — в канале.',
    'home.telegram.cta': 'Подписаться',

    // Section labels (used on listing pages + section badges)
    'section.pereezd.title': 'Переезд',
    'section.pereezd.lead': 'Виза, NIE/TIE, банк, медицина, школа — что узнать заранее и в каком порядке делать.',
    'section.zhizn.title': 'Жизнь',
    'section.zhizn.lead': 'Места, события, природа, гастро — то, ради чего сюда вообще ехать.',
    'section.biznes.title': 'Онлайн-работа',
    'section.biznes.lead': 'Только онлайн — удалённая работа, фриланс, autónomo. Налоги, LinkedIn, платформы (Upwork, Toptal, Contra, Malt), как искать заказы на трёх рынках: ЕС, США, СНГ. Без офлайна.',
    'section.ai.title': 'AI в работе и в жизни',
    'section.ai.lead': 'Чем AI реально помогает онлайн-предпринимателю и эмигранту: гиды, кейсы, видео. Внизу — наши продукты, если хочется глубже.',
    'section.back': '← Все материалы раздела',

    'about.title': 'Про меня',
    'footer.tagline': 'Жить у моря и работать удалённо — гайды, инструменты и опыт для тех, кто переезжает в Испанию или уже здесь.',
    'footer.sections': 'Разделы',
    'footer.contact': 'Связь',
    'footer.tg': 'Telegram-канал',
    'footer.ig': 'Instagram',
    'site.title.suffix': '· Kate in Spain',
    'site.title.default': 'Kate in Spain — жить у моря, работать удалённо',
    'site.desc.default': 'Гайды, инструменты и опыт для жизни у моря в Испании. Переезд, жизнь, бизнес и работа, AI-автоматизация.',
  },
  en: {
    'nav.home': 'Home',
    'nav.pereezd': 'Moving',
    'nav.zhizn': 'Life',
    'nav.biznes': 'Online work',
    'nav.ai': 'AI products',
    'nav.about': 'About',

    'home.hero.eyebrow': 'Kate in Spain',
    'home.hero.title': 'Live by the sea, work remotely',
    'home.hero.lead': 'Guides, tools and first-hand experience for people moving to Spain or already here. In the order it actually happens: arrive first, live first, then earn and grow.',
    'home.cta.primary': 'Where to start',
    'home.cta.telegram': 'Telegram channel',

    'home.sections.title': 'Four pillars',
    'home.sections.sub': 'In the order things actually happen: moving and life first, business and AI after.',

    'home.about.title': 'Who writes this',
    'home.about.sub': 'Kate — lives in Spain, runs a Telegram community and builds an AI Studio with her husband. Two threads in one place because I live both.',
    'home.about.cta': 'More',

    'home.telegram.title': 'Weekly — on Telegram',
    'home.telegram.sub': 'The site is the knowledge base. Fresh picks, events and short notes — on the channel.',
    'home.telegram.cta': 'Subscribe',

    'section.pereezd.title': 'Moving',
    'section.pereezd.lead': 'Visas, NIE/TIE, banking, healthcare, schools — what to know up front and the order to do it in.',
    'section.zhizn.title': 'Life',
    'section.zhizn.lead': 'Places, events, nature, food — the things that make any of this worth the move.',
    'section.biznes.title': 'Online work',
    'section.biznes.lead': 'Online only — remote work, freelancing, autónomo. Taxes, LinkedIn, platforms (Upwork, Toptal, Contra, Malt), how to land clients across three markets: EU, US, CIS. No offline.',
    'section.ai.title': 'AI for work and life',
    'section.ai.lead': 'How AI actually helps an online entrepreneur and an expat: guides, cases, video. Our products are at the bottom if you want to go deeper.',
    'section.back': '← All section articles',

    'about.title': 'About',
    'footer.tagline': 'Live by the sea, work remotely — guides, tools and experience for people moving to Spain or already here.',
    'footer.sections': 'Sections',
    'footer.contact': 'Contact',
    'footer.tg': 'Telegram channel',
    'footer.ig': 'Instagram',
    'site.title.suffix': '· Kate in Spain',
    'site.title.default': 'Kate in Spain — live by the sea, work remotely',
    'site.desc.default': 'Guides, tools and experience for life by the sea in Spain. Moving, life, business and work, AI.',
  },
} as const;

export type TranslationKey = keyof typeof ui.ru;

export function t(locale: Locale, key: TranslationKey): string {
  return (ui[locale] as Record<string, string>)[key] ?? (ui.ru as Record<string, string>)[key];
}

// Logical section id (RU slug) → URL slug per locale.
// `section` field in markdown frontmatter always uses RU slug = logical id.
export const sectionSlug = {
  ru: { pereezd: 'pereezd', zhizn: 'zhizn', biznes: 'biznes', ai: 'ai' },
  en: { pereezd: 'moving', zhizn: 'life', biznes: 'business', ai: 'ai' },
} as const;

// Full URL paths for top-level pages, by locale.
export const sectionPath = {
  ru: {
    home: '/',
    pereezd: '/pereezd/',
    zhizn: '/zhizn/',
    biznes: '/biznes/',
    ai: '/ai/',
    about: '/pro-menya/',
  },
  en: {
    home: '/en/',
    pereezd: '/en/moving/',
    zhizn: '/en/life/',
    biznes: '/en/business/',
    ai: '/en/ai/',
    about: '/en/about/',
  },
} as const;

// localeFromId extracts both the locale and the section+slug from a content id
// like "ru/pereezd/checklist-emigranta" or "en/moving/checklist-emigranta".
export function localeFromId(id: string): { locale: Locale; section: Section; slug: string } {
  const parts = id.split('/');
  const maybeLocale = parts[0];
  if (maybeLocale !== 'ru' && maybeLocale !== 'en') {
    throw new Error(`Content id missing locale prefix: ${id}`);
  }
  const locale: Locale = maybeLocale;
  const folder = parts[1];
  const slug = parts.slice(2).join('/');
  // Resolve folder name back to logical section id (always the RU slug).
  const sectionEntry = Object.entries(sectionSlug[locale]).find(([, s]) => s === folder);
  if (!sectionEntry) {
    throw new Error(`Unknown section folder "${folder}" in ${id}`);
  }
  return { locale, section: sectionEntry[0] as Section, slug };
}

export function altLocale(locale: Locale): Locale {
  return locale === 'ru' ? 'en' : 'ru';
}

// Logical section id (RU slug) used in nav highlight + frontmatter.
export type NavCurrent = 'home' | Section | 'about';
