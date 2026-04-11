---
description: Archive photos from git when their week is fully published. Photos stay on local disk.
---

# /archive_photos

Удаляет из git фото уже опубликованных недель. На локальном диске они остаются.

## Когда запускать

- Раз в неделю в воскресенье вечером (после публикации последнего поста недели)
- Или вручную когда видно что неделя полностью опубликована

## Что делает

1. Находит файлы `week*.json` где **все** posts со статусом `published`
2. Собирает все локальные фото из этих постов
3. Проверяет что фото не используется в других (неопубликованных) расписаниях
4. Удаляет из git index (`git rm --cached`) — но НЕ с диска
5. Добавляет пути в `.gitignore` чтобы не закоммитились снова
6. Сохраняет список архивированных фото в `content/photos/.archived-from-git.txt`

## Использование

```bash
# Сначала dry-run — увидеть что бы удалил
python scripts/archive_published_photos.py --dry

# Если всё ок — реально удалить
python scripts/archive_published_photos.py

# Закоммитить и запушить
git status
git commit -m "Archive photos from week N (still on disk)"
git push
```

## Важно

- Фото **остаются на твоём диске** — для будущего сайта
- Если будущий пост сошлётся на тот же файл — git добавит его обратно (.gitignore — это совет, не запрет)
- Список архивированных хранится в `content/photos/.archived-from-git.txt`
