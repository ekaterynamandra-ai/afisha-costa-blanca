---
description: Publish a specific post to Telegram right now, bypassing the schedule.
---

# /publish_now

Ручная публикация одного поста прямо сейчас, в обход cron-а.

## Использование

- `/publish_now w4-wed-1`
- `/publish_now w4-wed-1 --test` — в личку админа вместо канала (alias для test_mode)

## Обязательная проверка ПЕРЕД отправкой

**Запускай эти проверки в указанном порядке. Любая срывает публикацию до явного ОК Кати.**

1. **`git pull --no-rebase`** — обязательно, иначе риск дубликата с cron-постом. См. [[feedback_telegram_pull_before_publish]].

2. **Покажи Кате фото явно в чате (Read tool на файл).** Не публикуй пост, картинку которого Катя не утвердила в этой сессии. См. [[feedback_ask_about_photo_before_publish]]. Если в библиотеке нет ничего эстетичного — спроси: «генерим через Gemini / Pinterest-ссылку / переиспользуем X из библиотеки?».

3. **Проверь формат фото — должен быть landscape (aspect 1.3-1.8).** См. [[feedback_kostoplan_photo_format]]. Если вертикальная или квадратная — сначала кадрируй центр в 16:9 через PIL:
   ```python
   from PIL import Image
   img = Image.open(path)
   w, h = img.size
   target_aspect = 16/9
   if w/h < target_aspect:
       new_h = int(w / target_aspect)
       top = (h - new_h) // 2
       img.crop((0, top, w, top + new_h)).save(path)
   elif w/h > 2.5:
       new_w = int(h * target_aspect)
       left = (w - new_w) // 2
       img.crop((left, 0, left + new_w, h)).save(path)
   ```
   Сохрани кадрированную версию с новым именем (`*-landscape.jpg`), оригинал не трогай.

4. **Покажи финальное превью** (текст + слаг + размер фото). Жди явного «публикуй» / «ок».

## Что делает (после подтверждения)

1. Находит пост по ID во всех `week*.json` и standalone `post-*.json`
2. Показывает финальный preview (текст + фото)
3. **Ждёт подтверждения**: "опубликовать в @kate_in_spain? (да/нет)"
4. Запускает: `python scripts/publish_telegram.py --post-id <id>` ИЛИ напрямую `autopublish.send(text, photo)`
5. После успеха:
   - `status: published`
   - `published_at: <ISO>`
   - `message_id: <id из Telegram>`
6. **git commit + git push** (чтобы cron видел новый статус и не пересылал заново)
7. Если ошибка — показывает лог, не меняет status

## Когда использовать

- Срочный анонс (событие отменили / перенесли)
- GitHub Actions сломались, а пост надо
- После `/test_mode` — когда уже убедились, что всё ок
- Неделя не одобрена целиком, но один пост важно опубликовать

## Требования

- Локально должен быть Python 3 и установленные зависимости (см. scripts)
- `.env` в корне проекта с `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHANNEL` (chat_id, не username — см. [[reference]])
- Фото должно быть доступно: локальный файл существует или URL отдаёт 200
- Путь к фото в JSON — **относительно корня Costa Blanca** (например `content/photos/places/X.jpg` или `site/public/photos/covers/X.jpg`), не `./...`

## Если фото надо заменить ПОСЛЕ публикации

`editMessageMedia` API заменяет фото без перепубликации сообщения, caption остаётся:
```python
files = {'newphoto': open(path, 'rb')}
media = json.dumps({'type': 'photo', 'media': 'attach://newphoto'})
requests.post(
    f'https://api.telegram.org/bot{TOKEN}/editMessageMedia',
    data={'chat_id': CHANNEL, 'message_id': MID, 'media': media},
    files=files,
)
```

## Если пост уже published

Команда откажется публиковать второй раз. Сначала:
- Удалить сообщение в Telegram руками (или через `deleteMessage` API)
- `/update <id> status approved` (сбросить статус)
- Только потом `/publish_now`
