---
description: Edit an existing post in any week schedule.
---

# /update

Быстрое редактирование существующего поста в `content/schedule/week*.json`. Идёт сразу к нужному посту, без навигации по папкам.

## Использование

- `/update w4-wed-1` — по ID
- `/update 2026-04-22` — все посты на дату (для выбора)
- `/update w4-wed-1 text` — сразу редактировать текст
- `/update w4-wed-1 photo places/altea-iglesia-blue-domes.jpg` — поменять фото
- `/update w4-wed-1 time 19:00` — перенести время
- `/update w4-wed-1 delete` — удалить пост (спросит подтверждение)

## Что делает

1. Находит пост во всех `content/schedule/week*.json`
2. Показывает текущее состояние
3. Спрашивает, что менять (если аргумент не указан):
   - `text` / `title` / `photo` / `time` / `date` / `type` / `status` / `delete`
4. Применяет изменение
5. Регенерирует превью: `python scripts/generate_preview.py <файл>`
6. Если пост уже `published` — предупреждает: Telegram-сообщение не перепишется, меняется только JSON-архив

## Важно

- Подпись поста = первая строка. Если меняешь заголовок — меняй первую строку текста тоже
- После изменения approved-поста проверь, что валидный HTML (b/a/i закрыты)
- Если дата изменилась с уже-прошедшей на будущую — поменяй `status` с `published` на `draft` / `approved` вручную

## Примеры

```
/update w5-fri-1
→ что менять? (text/photo/time/...)

/update 2026-05-01
→ 2 поста на 1 мая:
  - w5-fri-1 · 10:00 · today_holiday
  - w5-fri-2 · 18:00 · audience_free
→ какой редактировать?
```
