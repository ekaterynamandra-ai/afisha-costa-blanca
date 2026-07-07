import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Single articles collection, sliced by `section` into the four site sections.
// File layout: src/content/articles/{ru,en}/<section-folder>/<slug>.md
// The first path segment is the locale, the second — section in that locale's
// own URL slug (pereezd/rabota/biznes/zhizn for RU, moving/work/business/life
// for EN). The `section` frontmatter field carries the LOGICAL section id
// (always the RU slug), used everywhere in code.
// Order here = display order across nav, homepage pillars, listings.
export const SECTIONS = ['pereezd', 'zhizn', 'biznes', 'ai'] as const;
export type Section = (typeof SECTIONS)[number];

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    section: z.enum(SECTIONS),
    date: z.coerce.date(),
    cover: z.string().optional(),
    tags: z.array(z.string()).default([]),
    reading_time: z.string().optional(),
    draft: z.boolean().default(false),
    // Optional event-specific fields (only used by section=zhizn for now)
    location: z.string().optional(),
    season: z.enum(['spring', 'summer', 'autumn', 'winter', 'year-round']).optional(),
    type: z.string().optional(),
    free: z.boolean().optional(),
  }),
});

export const collections = { articles };
