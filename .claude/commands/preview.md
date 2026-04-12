---
description: Generate HTML preview of a week schedule from JSON. Always synced with the actual schedule.
---

# /preview

Создаёт HTML preview недели из `content/schedule/week*.json`. Гарантирует что превью **всегда соответствует** реальному расписанию.

## Зачем

Раньше JSON и HTML preview расходились — я обновляла JSON, забывала обновить HTML, ты видела старые фото в preview. Теперь preview генерируется автоматически из JSON.

## Использование

```bash
# Сгенерировать превью для конкретного расписания
python scripts/generate_preview.py week3-apr-13-19.json

# С указанием выходного файла
python scripts/generate_preview.py week3-apr-13-19.json --output preview-week3.html
```

## Что делает

1. Читает `content/schedule/<file>.json`
2. Группирует посты по дням
3. Рендерит HTML с реальными фото (локальные пути → `../../content/photos/...`)
4. Сохраняет в `content/drafts/preview-<file>.html`

## Когда запускать

- **Каждый раз после изменения JSON** — чтобы preview синхронизировался
- Перед показом превью пользователю
- После замены фото

## Slash-вариант

Когда говоришь "сделай превью week3" — я запускаю:
```bash
python scripts/generate_preview.py week3-apr-13-19.json
```
