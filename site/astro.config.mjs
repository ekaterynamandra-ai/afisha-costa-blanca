// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://kateinspain.es',
  trailingSlash: 'always',
  build: {
    format: 'directory',
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
