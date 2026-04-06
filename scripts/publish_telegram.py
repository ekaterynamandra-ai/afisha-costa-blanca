"""
Публикация постов в Telegram-канал @afishaCB
Использование: python publish_telegram.py [--test] [--event EVENT_FILE]
"""

import json
import os
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Загрузка .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

EVENTS_DIR = Path(__file__).parent.parent / "content" / "events"


def send_message(text: str, photo_url: str = None, buttons: list = None) -> dict:
    """Отправить сообщение в канал."""

    # Inline-кнопки
    reply_markup = None
    if buttons:
        reply_markup = json.dumps({
            "inline_keyboard": [buttons]
        })

    if photo_url:
        # Пост с фото
        payload = {
            "chat_id": CHANNEL_ID,
            "photo": photo_url,
            "caption": text,
            "parse_mode": "HTML",
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        resp = requests.post(f"{API_BASE}/sendPhoto", data=payload)
    else:
        # Текстовый пост
        payload = {
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        resp = requests.post(f"{API_BASE}/sendMessage", data=payload)

    result = resp.json()
    if not result.get("ok"):
        print(f"ERROR: {result}")
    else:
        print(f"OK: message sent to {CHANNEL_ID}")
    return result


def format_audience_line(audience: list) -> str:
    """Форматировать строку аудитории с эмоджи."""
    audience_map = {
        "families": "👨‍👩‍👧 Семьям с детьми",
        "kids": "👶 С малышами",
        "teens": "🧑‍🤝‍🧑 Подросткам",
        "youth": "🎉 Молодёжи",
        "couples": "💑 Парам",
        "seniors": "🌿 Старшему поколению",
        "dogs": "🐕 С собаками",
        "solo": "🚶 Одному",
        "friends": "👯 Компанией",
        "photo": "📸 Фотографам",
        "foodies": "🍽️ Гурманам",
        "active": "🏃 Активным",
        "culture": "🎨 Любителям культуры",
        "all": "👥 Всем",
    }
    return " · ".join(audience_map.get(a, a) for a in audience)


def format_event_post(event: dict) -> str:
    """Форматировать событие в Telegram-пост (HTML)."""

    cat_emoji = event.get("category_emoji", "✨")
    category = event.get("category_name", "Событие")
    city = event.get("city", "")
    title = event.get("title", "")
    description = event.get("description", "")
    date = event.get("date", "")
    location = event.get("location", "")
    price = event.get("price", "Бесплатно")
    tip = event.get("tip", "")
    tags = event.get("tags", [])
    link = event.get("link", "")
    audience = event.get("audience", [])

    lines = []
    lines.append(f"{cat_emoji} <b>{category.upper()}</b> | {city}")
    lines.append("")
    lines.append(f"<b>{title}</b>")
    lines.append("")
    lines.append(description)
    lines.append("")
    lines.append(f"📅 {date}")
    lines.append(f"📍 {location}")
    lines.append(f"💰 {price}")

    if audience:
        lines.append("")
        lines.append(f"🎯 <b>Подойдёт:</b> {format_audience_line(audience)}")

    if tip:
        lines.append("")
        lines.append(f"💡 <b>Совет:</b> {tip}")

    if link:
        lines.append("")
        lines.append(f'🔗 <a href="{link}">Подробнее →</a>')

    if tags:
        lines.append("")
        lines.append(" ".join(f"#{t}" for t in tags))

    return "\n".join(lines)


def format_weekend_digest(events: list) -> str:
    """Форматировать дайджест выходных."""

    lines = []
    lines.append("🌟 <b>ЧТО ДЕЛАТЬ НА ВЫХОДНЫХ</b>")
    lines.append(events[0].get("weekend_dates", ""))
    lines.append("")

    num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

    for i, ev in enumerate(events[:7]):
        emoji = num_emojis[i] if i < len(num_emojis) else f"{i+1}."
        cat = ev.get("category_emoji", "✨")
        title = ev.get("title", "")
        city = ev.get("city", "")
        date_short = ev.get("date_short", "")
        price = ev.get("price", "Бесплатно")
        distance = ev.get("distance", "")

        lines.append(f"{emoji} <b>{cat} {title}</b> — {city}")
        lines.append(f"     📅 {date_short} · 💰 {price} · 📍 {distance}")
        lines.append("")

    lines.append("📱 <b>Подпишись, чтобы не пропустить!</b>")

    return "\n".join(lines)


def format_audience_digest(audience_key: str, events: list) -> str:
    """Подборка событий для конкретной аудитории."""

    audience_titles = {
        "families": ("👨‍👩‍👧 КУДА ПОЙТИ С ДЕТЬМИ", "Лучшие семейные события на Costa Blanca"),
        "youth": ("🎉 ДЛЯ МОЛОДЁЖИ", "Фестивали, концерты и движ на Costa Blanca"),
        "couples": ("💑 ДЛЯ ДВОИХ", "Романтичные события на Costa Blanca"),
        "dogs": ("🐕 С СОБАКОЙ", "Куда пойти с питомцем на Costa Blanca"),
        "foodies": ("🍽️ ДЛЯ ГУРМАНОВ", "Гастрособытия на Costa Blanca"),
        "active": ("🏃 ДЛЯ АКТИВНЫХ", "Спорт и активный отдых на Costa Blanca"),
        "culture": ("🎨 ДЛЯ ЦЕНИТЕЛЕЙ", "Культурные события на Costa Blanca"),
        "photo": ("📸 ДЛЯ ФОТОГРАФОВ", "Самые фотогеничные события Costa Blanca"),
        "free": ("🆓 БЕСПЛАТНО", "Лучшие бесплатные события Costa Blanca"),
    }

    title, subtitle = audience_titles.get(audience_key, ("📋 ПОДБОРКА", "События Costa Blanca"))

    lines = []
    lines.append(f"<b>{title}</b>")
    lines.append(f"<i>{subtitle}</i>")
    lines.append("")

    num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

    for i, ev in enumerate(events[:7]):
        emoji = num_emojis[i] if i < len(num_emojis) else f"{i+1}."
        cat = ev.get("category_emoji", "✨")
        title_ev = ev.get("title_short", ev.get("title", ""))
        city = ev.get("city", "")
        date_short = ev.get("date_short", ev.get("date", ""))
        price = ev.get("price", "Бесплатно")
        why = ev.get("why_this_audience", "")

        lines.append(f"{emoji} <b>{cat} {title_ev}</b>")
        lines.append(f"📍 {city} · 📅 {date_short} · 💰 {price}")
        if why:
            lines.append(f"→ <i>{why}</i>")
        lines.append("")

    lines.append("━━━━━━━━━━━━━")
    lines.append("📱 <b>Подпишись @afishaCB</b> — не пропусти интересное!")

    return "\n".join(lines)


def publish_event(event_file: str):
    """Опубликовать одно событие или дайджест из JSON-файла."""
    path = EVENTS_DIR / event_file
    with open(path, "r", encoding="utf-8") as f:
        event = json.load(f)

    # Определяем тип: дайджест или обычное событие
    if event.get("type") == "audience_digest":
        text = format_audience_digest(event["audience_key"], event["events"])
        photo = event.get("image_url")
    else:
        text = format_event_post(event)
        photo = event.get("image_url")

    buttons = []
    if event.get("link"):
        buttons.append({"text": "📱 Подробнее на сайте", "url": event["link"]})

    result = send_message(text, photo_url=photo, buttons=buttons if buttons else None)
    return result


def publish_all_pending():
    """Опубликовать все неопубликованные события."""
    if not EVENTS_DIR.exists():
        print(f"No events directory: {EVENTS_DIR}")
        return

    for f in sorted(EVENTS_DIR.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            event = json.load(fh)

        if event.get("published"):
            continue

        print(f"Publishing: {f.name}")
        result = publish_event(f.name)

        if result.get("ok"):
            # Помечаем как опубликованное
            event["published"] = True
            event["message_id"] = result["result"]["message_id"]
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(event, fh, ensure_ascii=False, indent=2)

        time.sleep(3)  # Пауза между постами


def test_connection():
    """Тест подключения к боту."""
    resp = requests.get(f"{API_BASE}/getMe")
    data = resp.json()
    if data.get("ok"):
        bot = data["result"]
        print(f"Bot: @{bot['username']} ({bot['first_name']})")
        print(f"Channel: {CHANNEL_ID}")
        print("Connection OK!")
    else:
        print(f"ERROR: {data}")
    return data


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set in .env")
        sys.exit(1)

    if "--test" in sys.argv:
        test_connection()
    elif "--draft" in sys.argv:
        # Публикация из папки drafts (готовые посты с текстом)
        idx = sys.argv.index("--draft") + 1
        if idx < len(sys.argv):
            draft_path = Path(__file__).parent.parent / "content" / "drafts" / sys.argv[idx]
            with open(draft_path, "r", encoding="utf-8") as f:
                draft = json.load(f)
            if not draft.get("approved"):
                print("WARNING: This draft is NOT approved! Add \"approved\": true first.")
                sys.exit(1)
            text = draft["text"]
            photo = draft.get("image_url")
            result = send_message(text, photo_url=photo)
            if result.get("ok"):
                draft["published"] = True
                draft["message_id"] = result["result"]["message_id"]
                with open(draft_path, "w", encoding="utf-8") as f:
                    json.dump(draft, f, ensure_ascii=False, indent=2)
    elif "--event" in sys.argv:
        idx = sys.argv.index("--event") + 1
        if idx < len(sys.argv):
            publish_event(sys.argv[idx])
    elif "--all" in sys.argv:
        publish_all_pending()
    else:
        print("Usage:")
        print("  python publish_telegram.py --test            # Test bot connection")
        print("  python publish_telegram.py --draft X.json    # Publish approved draft")
        print("  python publish_telegram.py --event X.json    # Publish one event")
        print("  python publish_telegram.py --all             # Publish all pending")
