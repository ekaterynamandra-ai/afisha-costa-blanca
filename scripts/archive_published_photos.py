"""
Архивация фото после публикации недели.

Что делает:
1. Находит файлы week*.json где ВСЕ посты опубликованы (status=published)
2. Собирает все фото которые использовались в этих постах
3. Удаляет их из git (но не с диска!)
4. Коммитит изменение

Логика:
- Фото остаются на твоём локальном диске (нужны для будущего сайта)
- Из git удаляются — освобождается место
- .gitignore блокирует их повторное добавление

Запуск:
    python scripts/archive_published_photos.py        # фактически удалить из git
    python scripts/archive_published_photos.py --dry  # показать что бы удалил
"""

import json
import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCHEDULE_DIR = PROJECT_ROOT / "content" / "schedule"
PHOTOS_DIR = PROJECT_ROOT / "content" / "photos" / "places"
GITIGNORE = PROJECT_ROOT / ".gitignore"
ARCHIVED_LIST = PROJECT_ROOT / "content" / "photos" / ".archived-from-git.txt"

DRY_RUN = "--dry" in sys.argv


def get_photos_from_post(post: dict) -> list[str]:
    """Собрать все локальные пути фото из поста (не URLs)."""
    photos = []
    photo = post.get("photo")
    if photo and not photo.startswith("http"):
        photos.append(photo)
    for p in post.get("photos", []) or []:
        if not p.startswith("http"):
            photos.append(p)
    return photos


def find_fully_published_weeks() -> list[Path]:
    """Найти недели где все posts published."""
    result = []
    if not SCHEDULE_DIR.exists():
        return result

    for f in sorted(SCHEDULE_DIR.glob("week*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            schedule = json.load(fh)

        posts = schedule.get("posts", [])
        if not posts:
            continue

        all_published = all(p.get("status") == "published" for p in posts)
        if all_published:
            result.append(f)
    return result


def collect_photos_to_archive(week_files: list[Path]) -> set[str]:
    """Собрать фото из опубликованных недель."""
    photos = set()
    for f in week_files:
        with open(f, "r", encoding="utf-8") as fh:
            schedule = json.load(fh)
        for post in schedule.get("posts", []):
            for photo_path in get_photos_from_post(post):
                photos.add(photo_path)
    return photos


def is_photo_used_elsewhere(photo: str, exclude_files: list[Path]) -> bool:
    """Проверить — используется ли фото в других расписаниях (не в опубликованных)."""
    for f in SCHEDULE_DIR.glob("week*.json"):
        if f in exclude_files:
            continue
        with open(f, "r", encoding="utf-8") as fh:
            schedule = json.load(fh)
        for post in schedule.get("posts", []):
            if photo in get_photos_from_post(post):
                return True
    return False


def add_to_gitignore(photos: set[str]):
    """Добавить пути в .gitignore чтобы не закоммитились снова."""
    existing = set()
    if GITIGNORE.exists():
        with open(GITIGNORE, "r", encoding="utf-8") as f:
            existing = set(line.strip() for line in f if line.strip())

    new_lines = []
    for p in sorted(photos):
        if p not in existing:
            new_lines.append(p)

    if new_lines:
        if DRY_RUN:
            print(f"  [DRY] Would add to .gitignore:")
            for line in new_lines:
                print(f"    {line}")
        else:
            with open(GITIGNORE, "a", encoding="utf-8") as f:
                f.write("\n# Archived after publication (still on disk)\n")
                for line in new_lines:
                    f.write(line + "\n")


def git_rm_cached(photos: set[str]) -> int:
    """Удалить из git index, но НЕ с диска (--cached)."""
    removed = 0
    for photo in sorted(photos):
        if not (PROJECT_ROOT / photo).exists():
            print(f"  ⏭ {photo} (not on disk, skipping)")
            continue

        if DRY_RUN:
            print(f"  [DRY] Would remove from git: {photo}")
            removed += 1
        else:
            try:
                subprocess.run(
                    ["git", "rm", "--cached", photo],
                    cwd=PROJECT_ROOT,
                    check=True,
                    capture_output=True
                )
                print(f"  ✅ Removed from git: {photo}")
                removed += 1
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ {photo}: {e.stderr.decode().strip()}")
    return removed


def save_archived_list(photos: set[str]):
    """Сохранить список архивированных фото для истории."""
    if DRY_RUN:
        return

    existing = set()
    if ARCHIVED_LIST.exists():
        with open(ARCHIVED_LIST, "r", encoding="utf-8") as f:
            existing = set(line.strip() for line in f if line.strip())

    all_archived = existing | photos

    ARCHIVED_LIST.parent.mkdir(parents=True, exist_ok=True)
    with open(ARCHIVED_LIST, "w", encoding="utf-8") as f:
        f.write("# Photos archived from git (still on disk locally)\n")
        f.write("# Format: relative path from project root\n\n")
        for p in sorted(all_archived):
            f.write(p + "\n")


def main():
    print("🔍 Looking for fully published weeks...")
    published_weeks = find_fully_published_weeks()

    if not published_weeks:
        print("  No fully published weeks found. Nothing to archive.")
        return

    print(f"  Found {len(published_weeks)} fully published week(s):")
    for w in published_weeks:
        print(f"    • {w.name}")

    print()
    print("📸 Collecting photos to archive...")
    photos_to_archive = collect_photos_to_archive(published_weeks)
    print(f"  Found {len(photos_to_archive)} photo(s) in published posts")

    # Filter out photos still used in non-published weeks
    photos_safe_to_remove = set()
    for photo in photos_to_archive:
        if is_photo_used_elsewhere(photo, published_weeks):
            print(f"  ⏭ {photo} (still used in unpublished weeks)")
        else:
            photos_safe_to_remove.add(photo)

    if not photos_safe_to_remove:
        print("  Nothing to archive (all photos still in use).")
        return

    print()
    print(f"🗑 Archiving {len(photos_safe_to_remove)} photo(s) from git...")
    removed = git_rm_cached(photos_safe_to_remove)

    print()
    print("📝 Updating .gitignore...")
    add_to_gitignore(photos_safe_to_remove)

    print()
    print("💾 Saving archived list...")
    save_archived_list(photos_safe_to_remove)

    print()
    print(f"{'='*50}")
    if DRY_RUN:
        print(f"DRY RUN: would archive {len(photos_safe_to_remove)} photos")
        print("Run without --dry to actually archive.")
    else:
        print(f"✅ Archived {removed} photos from git")
        print(f"   Photos still on disk at: content/photos/places/")
        print()
        print("Next steps:")
        print("  1. git status         # verify changes")
        print("  2. git commit -m '...'  # commit removal")
        print("  3. git push            # push to GitHub")


if __name__ == "__main__":
    main()
