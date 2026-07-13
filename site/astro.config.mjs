// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://kateinspain.es',
  // robots.txt already points at /sitemap-index.xml — this is what generates it.
  integrations: [sitemap()],
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  // The old hand-built checklist lived at /checklist.html and its URL is already
  // out in Telegram. Keep it alive, pointing at the native page.
  redirects: {
    '/checklist.html': '/checklist/',
  },
  i18n: {
    locales: ['ru', 'en'],
    defaultLocale: 'ru',
    routing: {
      prefixDefaultLocale: false,
      redirectToDefaultLocale: false,
    },
  },
});
