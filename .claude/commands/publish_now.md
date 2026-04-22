---
description: Publish a specific post to Telegram right now, bypassing the schedule.
---

# /publish_now

Ручная публикация одного поста прямо сейчас, в обход cron-а.

## Использование

- `/publish_now w4-wed-1`
- `/publish_now w4-wed-1 --test` — в личку админа вместо канала (alias для test_mode)

## Что делает

1. Находит пост по ID во всех `week*.json`
2. Показывает финальный preview (текст + фото)
3. **Ждёт подтверждения**: "опубликовать в @afishaCB? (да/нет)"
4. Запускает: `python scripts/publish_telegram.py --post-id w4-wed-1`
5. После успеха:
   - `status: published`
   - `published_at: <ISO>`
   - `message_id: <id из Telegram>`
6. Если ошибка — показывает лог, не меняет status

## Когда использовать

- Срочный анонс (событие отменили / перенесли)
- GitHub Actions сломались, а пост надо
- После `/test_mode` — когда уже убедились, что всё ок
- Неделя не одобрена целиком, но один пост важно опубликовать

## Требования

- Локально должен быть Python 3 и установленные зависимости (см. scripts)
- `.env` в корне проекта с `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHANNEL_ID`
- Фото должно быть доступно: локальный файл существует или URL отдаёт 200

## Если пост уже published

Команда откажется публиковать второй раз. Сначала:
- Удалить сообщение в Telegram руками (или через бот-API)
- `/update <id> status approved` (сбросить статус)
- Только потом `/publish_now`
