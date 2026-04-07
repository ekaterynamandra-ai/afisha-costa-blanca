"""
Автопубликация постов по расписанию.

Проверяет schedule/*.json, публикует посты с status="approved"
у которых дата+время <= сейчас, помечает как published.

Запуск: python autopublish.py
  - Вручную: запустить когда нужно
  - Автоматически: через cron / Task Scheduler / GitHub Actions

Логика:
  1. Читает все файлы schedule/*.json
  2. Проверяет: approved=true (неделя согласована)
  3. Для каждого поста: status="approved" и datetime <= now → публикует
  4. Обновляет status → "published", добавляет published_at
"""

import json
import os
import sys
import time
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# Все даты/время в расписании — по времени Испании (Europe/Madrid)
TZ_SPAIN = ZoneInfo("Europe/Madrid")

# Load .env if exists (local), otherwise use env vars (GitHub Actions)
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
SCHEDULE_DIR = Path(__file__).parent.parent / "content" / "schedule"

DRY_RUN = "--dry" in sys.argv
FORCE_TODAY = "--today" in sys.argv  # publish all approved posts for today regardless of time


PROJECT_ROOT = Path(__file__).parent.parent


def send(text, photo=None):
    """Отправить пост с одним фото или без."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would send: {text[:60]}...")
        return {"ok": True, "result": {"message_id": 0}}

    if photo:
        r = requests.post(f"{API}/sendPhoto", data={
            "chat_id": CHANNEL_ID, "photo": photo,
            "caption": text, "parse_mode": "HTML"
        })
    else:
        r = requests.post(f"{API}/sendMessage", data={
            "chat_id": CHANNEL_ID, "text": text,
            "parse_mode": "HTML", "disable_web_page_preview": True
        })

    d = r.json()
    if not d.get("ok") and photo:
        print(f"  Photo failed ({d.get('description','')}), retrying text-only...")
        r = requests.post(f"{API}/sendMessage", data={
            "chat_id": CHANNEL_ID, "text": text,
            "parse_mode": "HTML", "disable_web_page_preview": True
        })
        d = r.json()

    return d


def send_album(text, photos):
    """Отправить альбом (несколько фото) с подписью."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would send album ({len(photos)} photos): {text[:60]}...")
        return {"ok": True, "result": [{"message_id": 0}]}

    media = []
    files = {}

    for i, photo_path in enumerate(photos):
        if photo_path.startswith("http"):
            entry = {"type": "photo", "media": photo_path}
        else:
            full_path = Path(photo_path)
            if not full_path.is_absolute():
                full_path = PROJECT_ROOT / photo_path
            key = f"photo{i}"
            files[key] = open(full_path, "rb")
            entry = {"type": "photo", "media": f"attach://{key}"}

        if i == 0:
            entry["caption"] = text
            entry["parse_mode"] = "HTML"
        media.append(entry)

    r = requests.post(
        f"{API}/sendMediaGroup",
        data={"chat_id": CHANNEL_ID, "media": json.dumps(media)},
        files=files
    )
    d = r.json()

    for f in files.values():
        f.close()

    if not d.get("ok"):
        print(f"  Album failed ({d.get('description','')}), retrying single photo...")
        # Fallback: send first photo only
        first = photos[0]
        if first.startswith("http"):
            return send(text, photo=first)
        else:
            return send(text)

    return d


def notify_admin(published, skipped, errs, published_titles=None, tomorrow_titles=None):
    """Отправить отчёт админу в личку."""
    now_str = datetime.now(TZ_SPAIN).strftime("%d.%m.%Y %H:%M")
    lines = []

    if errs:
        lines.append(f"❌ <b>Ошибка публикации</b> ({now_str})")
        for e in errs:
            lines.append(f"• {e}")

    if published and published_titles:
        lines.append(f"\n✅ <b>Опубликовано сегодня ({published}):</b>")
        for t in published_titles:
            lines.append(f"• {t}")
    elif published:
        lines.append(f"✅ <b>Опубликовано: {published}</b> ({now_str})")

    if tomorrow_titles:
        lines.append(f"\n📅 <b>Завтра:</b>")
        for t in tomorrow_titles:
            lines.append(f"• {t}")

    if not lines:
        return "nothing to report"

    text = "\n".join(lines)

    try:
        r = requests.post(f"{API}/sendMessage", data={
            "chat_id": ADMIN_ID,
            "text": text,
            "parse_mode": "HTML"
        })
        return "sent" if r.json().get("ok") else r.json().get("description", "?")
    except Exception as e:
        return f"notify error: {e}"


def process_schedule():
    """Обработать все файлы расписания."""
    if not SCHEDULE_DIR.exists():
        print("No schedule directory found.")
        return

    now = datetime.now(TZ_SPAIN)
    tomorrow = (now + timedelta(days=1)).date()
    published_count = 0
    skipped_count = 0
    errors = []
    published_titles = []
    tomorrow_titles = []

    for f in sorted(SCHEDULE_DIR.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            schedule = json.load(fh)

        week_name = schedule.get("week", f.stem)

        if not schedule.get("approved"):
            print(f"\n⏸️  {week_name} — NOT APPROVED, skipping")
            continue

        print(f"\n✅ {week_name} — approved")

        for post in schedule.get("posts", []):
            post_id = post.get("id", "?")
            title = post.get("title", "???")
            status = post.get("status", "draft")

            if status == "published":
                continue

            if status != "approved":
                skipped_count += 1
                continue

            # Проверяем дату/время
            post_date = post.get("date", "")
            post_time = post.get("time", "10:00")
            try:
                post_dt = datetime.strptime(f"{post_date} {post_time}", "%Y-%m-%d %H:%M").replace(tzinfo=TZ_SPAIN)
            except ValueError:
                print(f"  ⚠️  #{post_id} {title} — bad date format, skipping")
                continue

            if post_dt > now:
                # --today: publish if same date, ignore time
                if FORCE_TODAY and post_dt.date() == now.date():
                    print(f"  🔵 #{post_id} {title} — today (forced)")
                else:
                    # Собираем завтрашние посты для отчёта
                    if post_dt.date() == tomorrow:
                        tomorrow_titles.append(f"{post_time} — {title}")
                    print(f"  ⏰ #{post_id} {title} — scheduled {post_date} {post_time} (not yet)")
                    skipped_count += 1
                    continue

            # Публикуем!
            text = post.get("text", "")
            if not text:
                print(f"  ⚠️  #{post_id} {title} — no text, skipping")
                continue

            photos = post.get("photos")  # album (list)
            photo = post.get("photo")    # single photo (string)
            print(f"  📤 #{post_id} {title}...")

            if photos and len(photos) > 1:
                result = send_album(text, photos)
            else:
                result = send(text, photo)

            if result.get("ok"):
                post["status"] = "published"
                post["published_at"] = now.isoformat()
                # Album returns list, single photo returns dict
                res = result.get("result", {})
                if isinstance(res, list) and len(res) > 0:
                    post["message_id"] = res[0].get("message_id")
                elif isinstance(res, dict):
                    post["message_id"] = res.get("message_id")
                published_count += 1
                published_titles.append(f"{post_time} — {title}")
                print(f"  ✅ Published!")

                # Сохраняем СРАЗУ после каждой публикации
                # чтобы при ошибке дальше пост не отправился повторно
                with open(f, "w", encoding="utf-8") as fh:
                    json.dump(schedule, fh, ensure_ascii=False, indent=2)
            else:
                err_msg = result.get('description', '?')
                errors.append(f"#{post_id} {title}: {err_msg}")
                print(f"  ❌ Failed: {err_msg}")

            time.sleep(4)  # Пауза между постами

        # Финальное сохранение (на случай если ничего не публиковалось)
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(schedule, fh, ensure_ascii=False, indent=2)

    print(f"\n{'='*40}")
    print(f"Published: {published_count} | Skipped/Waiting: {skipped_count}")
    if DRY_RUN:
        print("(DRY RUN — nothing was actually sent)")

    # Отправить отчёт админу в личку
    if ADMIN_ID and not DRY_RUN and (published_count > 0 or errors):
        report = notify_admin(published_count, skipped_count, errors, published_titles, tomorrow_titles)
        print(f"Admin report: {report}")


def show_status():
    """Показать статус всех постов."""
    if not SCHEDULE_DIR.exists():
        print("No schedule directory.")
        return

    for f in sorted(SCHEDULE_DIR.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            schedule = json.load(fh)

        week = schedule.get("week", f.stem)
        approved = "✅" if schedule.get("approved") else "⏸️"
        print(f"\n{approved} {week}")

        for post in schedule.get("posts", []):
            pid = post.get("id", "?")
            title = post.get("title", "?")
            date = post.get("date", "?")
            time_str = post.get("time", "?")
            status = post.get("status", "?")
            pub_at = post.get("published_at", "")

            icon = {"published": "✅", "approved": "🟢", "draft": "📝", "rejected": "❌"}.get(status, "❓")
            pub_info = f" (at {pub_at[:16]})" if pub_at else ""
            print(f"  {icon} #{pid} {date} {time_str} | {title}{pub_info}")


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set")
        sys.exit(1)

    if "--status" in sys.argv:
        show_status()
    elif "--approve" in sys.argv:
        # Quick approve: python autopublish.py --approve week2-apr-7-13.json
        idx = sys.argv.index("--approve") + 1
        if idx < len(sys.argv):
            fpath = SCHEDULE_DIR / sys.argv[idx]
            with open(fpath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            data["approved"] = True
            with open(fpath, "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
            print(f"✅ Approved: {sys.argv[idx]}")
    else:
        process_schedule()
