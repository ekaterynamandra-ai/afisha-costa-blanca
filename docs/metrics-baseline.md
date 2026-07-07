# kateinspain.es + @kate_in_spain — baseline metrics

Дата снапшота: **2026-07-07** (первый день M1 монетизационного плана).

Полный план: `C:\Users\ekate\.claude\plans\magical-tickling-spark.md`.

## Site

| Метрика | Значение | Источник |
|---------|----------|----------|
| Live URL | https://kateinspain.es | GitHub Pages |
| Публичных страниц (до M1 deploy) | 2 | `public/index.html` + `public/checklist.html` |
| Публичных страниц после M1 deploy | **55** | Astro build `site/dist/` |
| Sitemap.xml | нет | — |
| robots.txt | нет | 404 |
| Аналитика | нет | GoatCounter добавлен в M1, счётчик = 0 с 07.07.2026 |
| Email service | нет | Brevo — план M2 |
| Payments | нет | Gumroad — план M3 |
| Уникальных visits/мес | не измерялось | GoatCounter стартует |
| Sales до сегодня | 0 | нет продуктов |

## Telegram @kate_in_spain

| Метрика | Значение |
|---------|----------|
| Подписчиков | 77 |
| Постов/нед | 4 (v7 с 06.07.2026) |
| Время публикации | 10:00 (Europe/Madrid) |
| Cross-link на сайт до M1 | 0 постов |
| Cross-link из сайта на TG до M1 | broken (@afishaCB dead) |
| Cross-link из сайта на TG после M1 | все статьи + landing (`@kate_in_spain`) |

## Готовые ассеты (что реюзаем)

| Ассет | Файл | Роль в плане |
|-------|------|--------------|
| Чек-лист переезда | `public/checklist.pdf` + `.html` | Tier 0 lead magnet (M2 gate за email) |
| Ипотечный Google Sheet | msg 185 в TG (26.06.2026) | Tier 1 core (M3 €12 продукт) |
| Пост про обмен прав DGT | live в TG | Playbook глава «Документы» (M5) |
| Пост про autonomo налоги | live в TG | Playbook глава «Финансы» (M5) |
| 43 статьи в `site/` (ru) | ai=3 / biznes=5 / pereezd=8 / zhizn=27 | Все выходят в M1 |
| Формат v7 | week16-jul-6-12.json | Ежедневный контент → SEO + email pipeline |

## Цели М1 (07.2026)

- Astro сайт live: 55 страниц вместо 2 ✓
- 0 мёртвых afishaCB в live-коде ✓
- GoatCounter установлен, baseline visits записан ✓
- TgCta компонент на всех статьях ✓
- Checklist карточка на homepage ✓

## Цели М2 (08.2026)

- TG: 200+ подписчиков (было 77)
- Emails: 60+ капчей через Brevo
- Site: 500+ unique visits/мес по GoatCounter
- 0 хардкоденых WHITELIST в `import_telegram_to_zhizn.py`

## Цели М3 (09.2026)

- Ипотечный продукт €12 live на Gumroad
- 10+ продаж (€120+ revenue)
- TG: 300+ подписчиков
- Emails: 120+ капчей
- Site: 5000+ pageviews/мес

## Кому смотреть

- **GoatCounter** dashboard: https://kateinspain.goatcounter.com (регистрация нужна после deploy)
- **TG @kate_in_spain**: t.me/kate_in_spain
- **Brevo** (после M2): mailin.brevo.com
- **Gumroad** (после M3): gumroad.com/kateinspain
