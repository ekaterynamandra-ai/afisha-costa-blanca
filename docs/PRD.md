


























# Product Requirements Document (PRD)
# Афиша Costa Blanca

**Версия:** 1.0 MVP
**Дата:** 2026-04-05
**Автор:** Ekaterina + Claude Code

---

## 1. Обзор продукта

### 1.1 Проблема
Русскоговорящие экспаты на Costa Blanca (50K-100K+ человек) пропускают интересные местные события, потому что:
- Информация только на испанском
- Разбросана по десяткам муниципальных сайтов
- Нет единого агрегатора с фильтрами
- В Telegram-чатах события тонут среди объявлений

### 1.2 Решение
Двуязычный (RU/EN) агрегатор событий Costa Blanca:
- **Telegram-канал** — пуш-уведомления о лучших событиях
- **Веб-сайт** — каталог с фильтрами, поиском, деталями
- **Автоматизация** — парсинг источников + Claude API перевод

### 1.3 Целевая аудитория
| Сегмент | Описание | Потребность |
|---------|----------|------------|
| Экспаты-семьи | Русские семьи с детьми, живущие на побережье | Детские и семейные мероприятия |
| Молодые экспаты | 25-40 лет, активный образ жизни | Фестивали, концерты, спорт |
| Пенсионеры | Зимовщики и постоянные резиденты | Культура, природа, гастрономия |
| Туристы | Краткосрочные визиты | Что посмотреть за выходные |

### 1.4 Уникальное ценностное предложение
"Все лучшие события Costa Blanca на русском языке — с практическими советами, в одном месте."

---

## 2. Функциональные требования

### 2.1 Telegram-канал (MVP — приоритет 1)

#### Типы контента
| Тип | Частота | Описание |
|-----|---------|----------|
| Одиночное событие | 1-3 в день | Отдельный пост о ярком событии |
| Дайджест выходных | Пт вечер | Топ-5 событий на Сб-Вс |
| Срочное | По ситуации | "Сегодня! Бесплатный концерт..." |
| Дайджест недели | Пн утро | Обзор предстоящей недели |

#### Формат поста (одиночное событие)
```
{emoji_категории} {КАТЕГОРИЯ} | {Город}

{Заголовок — 1 строка, цепляющий}

{Описание — 2-3 предложения, живой стиль}

📅 {дата и время}
📍 {город} ({расстояние от Аликанте})
💰 {цена}

💡 Совет: {практический совет}

🔗 Подробнее: {ссылка на сайт}

#{тег1} #{тег2} #{тег3} #CostaBlanca
```

#### Telegram-бот (функционал)
- Публикация постов в канал через Bot API
- Форматирование: Markdown (bold, italic, ссылки)
- Inline-кнопки: "Подробнее на сайте", "Поделиться"
- Фото к посту (image_url из БД)

---

### 2.2 Веб-сайт (MVP — приоритет 2)

#### Технологии
| Компонент | Технология |
|-----------|-----------|
| Frontend | React + TypeScript + Tailwind CSS (через Lovable) |
| Backend/DB | Supabase (PostgreSQL + Auth + Storage + REST API) |
| Хостинг | Lovable (*.lovable.app) → потом свой домен |
| Роутинг | React Router |
| Иконки | Lucide React + эмоджи |

#### Страницы

**Главная (/)**
- Hero-секция с заголовком и CTA
- "На этих выходных" — 3 карточки (status=published, ближайшие Сб-Вс, ORDER BY interest_score DESC)
- "Скоро" — 8 карточек (следующие 30 дней, ORDER BY event_date ASC)
- Категории — кликабельные чипы с эмоджи
- Telegram CTA — блок подписки

**Каталог (/events)**
- Фильтры: категория, дата (неделя/месяц/диапазон), расстояние, текстовый поиск
- Карточки в сетке (2 колонки десктоп, 1 мобайл)
- Пагинация или "Загрузить ещё"
- URL-параметры: /events?category=festival&distance=60
- Счётчик: "Найдено X событий"

**Детали события (/events/:slug)**
- Большое фото
- Бэйдж категории
- Инфо-карточки: место, дата, цена
- Полное описание
- Блок "Совет" (выделенный)
- Google Maps embed (если есть координаты)
- Ссылка на источник
- Кнопки: "Поделиться в Telegram", "Скопировать ссылку"
- Похожие события (та же категория, 3 шт)

**Админ-панель (/admin)**
- Защита через Supabase Auth (email + пароль)
- Дашборд: счётчики (черновики, на ревью, опубликовано)
- Таблица событий: сортировка, фильтрация, быстрые действия
- Редактор события: все поля + превью Telegram-поста
- Кнопки: "Сохранить", "Сохранить и опубликовать"
- Ручное добавление события

#### Дизайн-система
| Токен | Значение | Применение |
|-------|----------|-----------|
| Primary | `#1A365D` | Навигация, заголовки |
| Accent | `#F6AD55` | CTA, кнопки |
| Background | `#FFFAF0` | Фон страниц |
| Card BG | `#FFFFFF` | Карточки |
| Text | `#2D3748` | Основной текст |
| Muted | `#718096` | Вторичный текст |
| Link | `#2B6CB0` | Ссылки |
| Success | `#38A169` | "Бесплатно" |
| Radius | `14px` | Карточки |
| Shadow | `0 2px 8px rgba(0,0,0,0.06)` | Карточки |

**Принципы:**
- Mobile-first
- Средиземноморский стиль: тёплые тона, чистый дизайн
- "Airbnb Experiences meets журнал"
- Шрифт: Inter
- Карточки: скругления, лёгкая тень, hover-эффект

---

### 2.3 Автоматизация (MVP — приоритет 3)

#### Архитектура (без n8n, чисто Python/TS)

```
GitHub Actions (cron)
  │
  ├── 08:00 daily ──→ fetch_events.py
  │                     ├── RSS: alicante.es, costablancaup.com
  │                     ├── API: comunitatvalenciana.com, Eventbrite
  │                     ├── Scrape: hoyalicante.app
  │                     └── → Supabase INSERT (status='raw')
  │
  ├── 09:00 daily ──→ process_events.py
  │                     ├── Claude API: перевод ES→RU
  │                     ├── Генерация: short_description, telegram_post
  │                     ├── Оценка: interest_score (1-10)
  │                     └── → Supabase UPDATE (status='draft')
  │
  ├── */15 min ────→ publish_telegram.py
  │                     ├── SELECT WHERE status='approved' AND telegram_published=false
  │                     ├── Telegram Bot API: публикация
  │                     └── → UPDATE telegram_published=true
  │
  ├── Fri 18:00 ───→ weekend_digest.py
  │                     ├── SELECT WHERE event_date IN (Sat, Sun)
  │                     ├── Формирование дайджеста
  │                     └── → Telegram: пост-дайджест
  │
  └── 00:00 daily ──→ archive_events.py
                        └── UPDATE status='archived' WHERE event_date < today
```

#### Скрипты

**fetch_events.py**
- Input: 7 источников (RSS, API, scraping)
- Дедупликация: по (title + event_date) или (source_url)
- Output: Supabase INSERT с status='raw'
- Логирование: сколько найдено, сколько новых, ошибки

**process_events.py**
- Input: events WHERE status='raw'
- Claude API промпт:
  ```
  Ты — редактор русскоязычной афиши Costa Blanca.
  Исходные данные: {raw event JSON}
  
  Задачи:
  1. Переведи title и description на русский
  2. Напиши short_description (1-2 предложения, цепляющие)
  3. Определи category из списка: festival, nature, gastro, kids, music, market, sport, culture, fireworks, other
  4. Оцени interest_score (1-10): насколько это интересно русскоязычному экспату?
  5. Напиши telegram_post по шаблону
  6. Напиши практический совет (tips)
  7. Переведи title и description на английский
  
  Формат ответа: JSON
  ```
- Output: Supabase UPDATE с заполненными полями, status='draft'

**publish_telegram.py**
- Telegram Bot API: sendMessage / sendPhoto
- Форматирование: MarkdownV2
- Inline keyboard: [Подробнее →] (ссылка на сайт)
- Rate limiting: не чаще 1 поста в 3 минуты

**weekend_digest.py**
- Собирает approved/published события на Сб-Вс
- Сортирует по interest_score
- Берёт топ-5
- Форматирует дайджест-пост

---

## 3. База данных

### 3.1 Таблица: events (упрощённая для MVP)

```sql
CREATE TABLE events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Контент (RU)
  title_ru TEXT NOT NULL,
  description_ru TEXT,
  short_description_ru TEXT,
  tips_ru TEXT,
  telegram_post_ru TEXT,

  -- Контент (EN)
  title_en TEXT,
  description_en TEXT,
  short_description_en TEXT,
  tips_en TEXT,

  -- Место
  city TEXT NOT NULL,
  city_en TEXT,
  address TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  distance_minutes INTEGER,  -- минуты от Аликанте (для фильтра)

  -- Время
  event_date DATE NOT NULL,
  event_date_end DATE,
  event_time TEXT,

  -- Метаданные
  category TEXT NOT NULL DEFAULT 'other',
  tags TEXT[],
  price TEXT,
  price_en TEXT,
  image_url TEXT,
  source_url TEXT,
  slug TEXT UNIQUE,

  -- Telegram
  telegram_published BOOLEAN DEFAULT FALSE,
  telegram_published_at TIMESTAMPTZ,

  -- Управление
  status TEXT NOT NULL DEFAULT 'raw'
    CHECK (status IN ('raw', 'draft', 'review', 'approved', 'published', 'rejected', 'archived')),
  interest_score INTEGER CHECK (interest_score BETWEEN 1 AND 10)
);

-- Индексы
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_category ON events(category);
CREATE INDEX idx_events_slug ON events(slug);
CREATE INDEX idx_events_tg ON events(telegram_published) WHERE telegram_published = false;
```

### 3.2 Таблица: categories

```sql
CREATE TABLE categories (
  id TEXT PRIMARY KEY,
  name_ru TEXT NOT NULL,
  name_en TEXT NOT NULL,
  icon TEXT,
  color TEXT,
  sort_order INTEGER DEFAULT 0
);

INSERT INTO categories VALUES
  ('festival', 'Фестивали', 'Festivals', '🎭', '#E74C3C', 1),
  ('nature', 'Природа', 'Nature', '🌸', '#27AE60', 2),
  ('gastro', 'Гастрономия', 'Food & Drink', '🍷', '#F39C12', 3),
  ('kids', 'Для детей', 'For Kids', '👨‍👩‍👧‍👦', '#3498DB', 4),
  ('music', 'Музыка', 'Music', '🎵', '#9B59B6', 5),
  ('market', 'Рынки и ярмарки', 'Markets & Fairs', '🛍️', '#E67E22', 6),
  ('sport', 'Спорт', 'Sports', '⚽', '#1ABC9C', 7),
  ('culture', 'Культура', 'Culture', '🏛️', '#8E44AD', 8),
  ('fireworks', 'Фейерверки', 'Fireworks', '🎆', '#E91E63', 9),
  ('other', 'Другое', 'Other', '✨', '#95A5A6', 10);
```

### 3.3 RLS Policies

```sql
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Публичный доступ: только published
CREATE POLICY "Public read published" ON events
  FOR SELECT USING (status = 'published');

-- Админ: полный доступ
CREATE POLICY "Admin full access" ON events
  FOR ALL USING (auth.role() = 'authenticated');
```

### 3.4 Таблица: event_sources (трекинг источников)

```sql
CREATE TABLE event_sources (
  id TEXT PRIMARY KEY,     -- 'alicante_rss', 'costablancaup', etc.
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  type TEXT NOT NULL,      -- 'rss', 'api', 'scrape'
  active BOOLEAN DEFAULT TRUE,
  last_fetched TIMESTAMPTZ,
  events_found INTEGER DEFAULT 0,
  errors INTEGER DEFAULT 0
);
```

---

## 4. Языковая система

### 4.1 Подход
- Все тексты хранятся в двух вариантах: `*_ru` и `*_en`
- UI-тексты в JSON-файле (i18n)
- Язык по умолчанию: русский
- Сохранение в localStorage
- Переключатель в шапке: [RU | EN]

### 4.2 Перевод событий
- Источники на ES → Claude API → RU + EN
- Источники на EN → Claude API → RU (EN оставляем)
- Ручной ввод: админ заполняет RU, EN опционально

---

## 5. Интеграции

### 5.1 Claude API
- **Модель**: claude-sonnet-4-6 (баланс качества и стоимости)
- **Задачи**: перевод, форматирование, оценка, генерация советов
- **Оценка расхода**: ~$0.01-0.03 на событие, ~$3-10/мес при 300 событиях

### 5.2 Telegram Bot API
- **Бот**: @AfishaCostaBlancanBot (создать через @BotFather)
- **Канал**: @AfishaCostaBlanка (создать)
- **Формат**: MarkdownV2 + фото + inline-кнопки
- **Лимиты**: 30 сообщений/сек в канал (более чем достаточно)

### 5.3 Supabase
- **Plan**: Free (500MB DB, 1GB Storage, 50K auth MAU)
- **API**: REST для скриптов, JS SDK для фронтенда
- **Auth**: email/password для админки
- **Storage**: фото событий (если нет внешнего URL)

### 5.4 GitHub Actions
- **Plan**: Free (2000 мин/мес)
- **Cron jobs**: 4 скрипта по расписанию
- **Secrets**: SUPABASE_URL, SUPABASE_KEY, CLAUDE_API_KEY, TELEGRAM_BOT_TOKEN

---

## 6. Что НЕ входит в MVP

| Фича | Почему нет | Когда добавить |
|------|-----------|---------------|
| Регистрация пользователей | Нет необходимости, открытый доступ | v2 (если нужна персонализация) |
| Комментарии/отзывы | Усложняет модерацию | v2 |
| Карта всех событий | Сложная интеграция | v2 |
| Email-рассылка | Аудитория в Telegram | v3 |
| Оплата/билеты | Не агрегатор билетов | Никогда (ссылка на оригинал) |
| SEO-мета теги | Не критично для MVP | v1.1 |
| PWA/мобильное приложение | Telegram + веб достаточно | v3 |
| Аналитика подробная | Базовая Supabase достаточно | v1.1 |
| Блог | Отвлекает от основного | v2 |
| Instagram-интеграция | Telegram приоритетнее | v2 |

---

## 7. Метрики успеха (через 1 месяц после запуска)

| Метрика | Цель |
|---------|------|
| Telegram-подписчики | 200+ |
| Уникальные посетители сайта / мес | 500+ |
| События в базе | 100+ |
| Автоматизированных событий | 70%+ (vs ручной ввод) |
| Средний охват поста в Telegram | 100+ просмотров |

---

## 8. Расходы (оценка MVP)

| Статья | Стоимость | Комментарий |
|--------|-----------|-------------|
| Supabase | $0 | Free plan |
| Claude API | ~$5-10/мес | Перевод 300 событий |
| Домен | ~$10-15/год | .com или .es |
| Lovable | $0-20/мес | Free или Starter |
| GitHub Actions | $0 | Free tier |
| Telegram | $0 | Бесплатно |
| **Итого** | **~$10-30/мес** | |

---

## 9. Timeline

### Неделя 1: Фундамент
- [ ] Создать Supabase проект + таблицы + RLS
- [ ] Создать Telegram канал + бот
- [ ] Создать сайт в Lovable (промпт из этого PRD)
- [ ] Подключить Supabase к Lovable
- [ ] Добавить 10 событий вручную для тестирования

### Неделя 2: Автоматизация
- [ ] Написать fetch_events.py (Tier 1 источники: 3 шт)
- [ ] Написать process_events.py (Claude API интеграция)
- [ ] Написать publish_telegram.py
- [ ] Настроить GitHub Actions cron
- [ ] Тестирование полного цикла

### Неделя 3: Контент и доработка
- [ ] Добавить Tier 2 источники (ещё 3)
- [ ] Написать weekend_digest.py
- [ ] Доработка дизайна сайта по результатам
- [ ] Наполнение: 30+ событий
- [ ] Тестирование на мобильных

### Неделя 4: Запуск
- [ ] Подключить свой домен
- [ ] Первый пост в Telegram
- [ ] Распространение в русскоязычных группах (3-5)
- [ ] Первый пятничный дайджест
- [ ] Мониторинг + фикс багов

---

## 10. Приложения

### 10.1 Промпт для Lovable
См. отдельный файл: `lovable-prompt.md`

### 10.2 Макеты
- Telegram-посты: `mockup-telegram.html` (открыть в браузере)
- Веб-сайт: `mockup-website.html` (открыть в браузере)

### 10.3 Анализ
- Критический анализ: `01-analysis.md`
- План скиллов: `02-skills-plan.md`
