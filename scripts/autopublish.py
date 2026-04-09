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


def send(text, photo=None, test_mode=False):
    """Отправить пост с одним фото или без. test_mode=True → отправка админу в личку."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would send: {text[:60]}...")
        return {"ok": True, "result": {"message_id": 0}}

    target = ADMIN_ID if test_mode else CHANNEL_ID
    if test_mode:
        text = f"🧪 <b>ТЕСТ:</b>\n\n{text}"

    if photo:
        r = requests.post(f"{API}/sendPhoto", data={
            "chat_id": target, "photo": photo,
            "caption": text, "parse_mode": "HTML"
        })
    else:
        r = requests.post(f"{API}/sendMessage", data={
            "chat_id": target, "text": text,
            "parse_mode": "HTML", "disable_web_page_preview": True
        })

    d = r.json()
    if not d.get("ok") and photo:
        print(f"  Photo failed ({d.get('description','')}), retrying text-only...")
        r = requests.post(f"{API}/sendMessage", data={
            "chat_id": target, "text": text,
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


def send_admin(text):
    """Отправить сообщение админу в личку."""
    if not ADMIN_ID or DRY_RUN:
        print(f"  [ADMIN] {text[:80]}...")
        return
    try:
        requests.post(f"{API}/sendMessage", data={
            "chat_id": ADMIN_ID, "text": text, "parse_mode": "HTML"
        })
    except Exception as e:
        print(f"  Admin notify error: {e}")


def notify_published(title, next_post=None, tomorrow_posts=None, is_last_today=False):
    """Отчёт после каждой публикации."""
    now_str = datetime.now(TZ_SPAIN).strftime("%H:%M")
    lines = [f"✅ <b>Опубликовано</b> ({now_str}):", f"• {title}"]

    if is_last_today and tomorrow_posts:
        lines.append(f"\n📅 <b>Завтра:</b>")
        for t in tomorrow_posts:
            lines.append(f"• {t}")
    elif next_post:
        lines.append(f"\n⏭ <b>Следующий:</b> {next_post}")

    send_admin("\n".join(lines))


def notify_error(title, error_msg):
    """Отчёт об ошибке."""
    now_str = datetime.now(TZ_SPAIN).strftime("%H:%M")
    send_admin(f"❌ <b>Ошибка публикации</b> ({now_str})\n• {title}\n• {error_msg}")


def check_planning_reminders():
    """Напоминания о планировании."""
    now = datetime.now(TZ_SPAIN)
    today = now.date()
    reminders = []

    # Собираем все недели
    approved_ends = []
    unapproved_weeks = []
    all_ends = []

    for f in sorted(SCHEDULE_DIR.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            schedule = json.load(fh)
        week = schedule.get("week", "")
        if " to " not in week:
            continue
        end_str = week.split(" to ")[1].strip()
        try:
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        all_ends.append(end_date)
        if schedule.get("approved"):
            approved_ends.append(end_date)
        else:
            unapproved_weeks.append(week)

    last_approved = max(approved_ends) if approved_ends else None
    last_any = max(all_ends) if all_ends else None

    # Проверяем статус планирования
    if last_approved:
        days_covered = (last_approved - today).days

        if days_covered > 14:
            # Всё ок, план есть на 2+ недели вперёд
            reminders.append(f"✅ <b>План одобрен</b> до {last_approved.strftime('%d.%m.%Y')} ({days_covered} дней)")
        elif days_covered > 2:
            # План есть, но скоро кончится
            if unapproved_weeks:
                reminders.append(f"📋 Есть неутверждённый план — нужно согласовать!")
            else:
                reminders.append(f"✅ План одобрен до {last_approved.strftime('%d.%m.%Y')} ({days_covered} дн.)")
        else:
            # Критично — план заканчивается
            if unapproved_weeks:
                reminders.append(f"⚠️ <b>Срочно:</b> план заканчивается {last_approved.strftime('%d.%m')}! Есть черновик — нужно согласовать!")
            else:
                reminders.append(f"⚠️ <b>Срочно:</b> план заканчивается {last_approved.strftime('%d.%m')}! Нужен план на следующую неделю!")
    else:
        reminders.append("⚠️ <b>Нет одобренного плана!</b> Нужно согласовать расписание.")

    # Напоминание: план на месяц (25-е число)
    if today.day >= 25:
        next_month_date = today.replace(day=1) + timedelta(days=32)
        month_names_ru = {
            1: "январь", 2: "февраль", 3: "март", 4: "апрель",
            5: "май", 6: "июнь", 7: "июль", 8: "август",
            9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
        }
        next_month = month_names_ru.get(next_month_date.month, "?")

        # Проверяем есть ли план на следующий месяц
        next_month_start = next_month_date.replace(day=1)
        has_next_month = last_any and last_any >= next_month_start
        if has_next_month:
            reminders.append(f"📅 План на {next_month} — есть ✅")
        else:
            reminders.append(f"📅 <b>Напоминание:</b> конец месяца — пора сделать план на {next_month}!")

    if reminders:
        send_admin("\n".join(reminders))


def process_schedule():
    """Обработать все файлы расписания."""
    if not SCHEDULE_DIR.exists():
        print("No schedule directory found.")
        return

    now = datetime.now(TZ_SPAIN)
    tomorrow = (now + timedelta(days=1)).date()
    published_count = 0
    skipped_count = 0

    # Собираем ВСЕ одобренные посты для анализа "что дальше"
    all_approved = []
    for f in sorted(SCHEDULE_DIR.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            schedule = json.load(fh)
        if not schedule.get("approved"):
            continue
        for post in schedule.get("posts", []):
            if post.get("status") == "approved":
                post["_file"] = str(f)
                all_approved.append(post)

    # Сортируем по дате
    def post_sort_key(p):
        return f"{p.get('date','')} {p.get('time','10:00')}"
    all_approved.sort(key=post_sort_key)

    # Завтрашние посты
    tomorrow_posts = [
        f"{p.get('time','10:00')} — {p.get('title','?')}"
        for p in all_approved
        if p.get("date", "") == str(tomorrow)
    ]

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
            post_time = post.get("time", "10:00")

            if status == "published":
                continue

            if status != "approved":
                skipped_count += 1
                continue

            # Проверяем дату/время
            post_date = post.get("date", "")
            try:
                post_dt = datetime.strptime(f"{post_date} {post_time}", "%Y-%m-%d %H:%M").replace(tzinfo=TZ_SPAIN)
            except ValueError:
                print(f"  ⚠️  #{post_id} {title} — bad date format, skipping")
                continue

            if post_dt > now:
                if FORCE_TODAY and post_dt.date() == now.date():
                    print(f"  🔵 #{post_id} {title} — today (forced)")
                else:
                    print(f"  ⏰ #{post_id} {title} — scheduled {post_date} {post_time} (not yet)")
                    skipped_count += 1
                    continue

            # Публикуем!
            text = post.get("text", "")
            if not text:
                print(f"  ⚠️  #{post_id} {title} — no text, skipping")
                continue

            photos = post.get("photos")
            photo = post.get("photo")
            print(f"  📤 #{post_id} {title}...")

            if photos and len(photos) > 1:
                result = send_album(text, photos)
            else:
                test_mode = post.get("test_mode", False)
                result = send(text, photo, test_mode=test_mode)

            if result.get("ok"):
                post["status"] = "published"
                post["published_at"] = now.isoformat()
                res = result.get("result", {})
                if isinstance(res, list) and len(res) > 0:
                    post["message_id"] = res[0].get("message_id")
                elif isinstance(res, dict):
                    post["message_id"] = res.get("message_id")
                published_count += 1
                print(f"  ✅ Published!")

                # Сохраняем СРАЗУ
                with open(f, "w", encoding="utf-8") as fh:
                    json.dump(schedule, fh, ensure_ascii=False, indent=2)

                # Определяем: это последний пост сегодня?
                remaining_today = [
                    p for p in all_approved
                    if p.get("date") == post_date
                    and p.get("status") == "approved"
                    and p.get("id") != post_id
                ]
                # Убираем текущий из списка
                all_approved = [p for p in all_approved if p.get("id") != post_id]

                is_last_today = len(remaining_today) == 0

                # Следующий пост (если не последний сегодня)
                next_post = None
                if not is_last_today and remaining_today:
                    np = remaining_today[0]
                    next_post = f"{np.get('time','?')} — {np.get('title','?')}"

                # Отчёт после каждого поста
                notify_published(
                    title=f"{post_time} — {title}",
                    next_post=next_post,
                    tomorrow_posts=tomorrow_posts if is_last_today else None,
                    is_last_today=is_last_today
                )
            else:
                err_msg = result.get('description', '?')
                notify_error(title, err_msg)
                print(f"  ❌ Failed: {err_msg}")

            time.sleep(4)

        # Финальное сохранение
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(schedule, fh, ensure_ascii=False, indent=2)

    print(f"\n{'='*40}")
    print(f"Published: {published_count} | Skipped/Waiting: {skipped_count}")

    # Напоминания о планировании — только если что-то опубликовалось
    # (чтобы не спамить каждый час когда нечего публиковать)
    if published_count > 0:
        check_planning_reminders()


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
