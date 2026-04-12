"""
Генерирует HTML превью из расписания week*.json.

Это гарантирует что превью всегда соответствует реальному расписанию —
никогда не будет ситуации "в JSON одно, в HTML другое".

Использование:
    python scripts/generate_preview.py week3-apr-13-19.json
    python scripts/generate_preview.py week3-apr-13-19.json --output preview-week3.html
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCHEDULE_DIR = PROJECT_ROOT / "content" / "schedule"
DRAFTS_DIR = PROJECT_ROOT / "content" / "drafts"

WEEKDAY_NAMES_RU = {
    0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб", 6: "Вс"
}

MONTH_NAMES_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
    7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}


def format_date(date_str: str) -> str:
    """2026-04-13 → Пн 13 апр"""
    from datetime import datetime
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{WEEKDAY_NAMES_RU[d.weekday()]} {d.day} {MONTH_NAMES_RU[d.month][:3]}"
    except ValueError:
        return date_str


def html_escape(text: str) -> str:
    """Минимальный escape — оставляем HTML теги для bold/links."""
    # text уже содержит <b>, <a>, <br>
    return text


def render_post(post: dict, idx: int) -> str:
    """Рендер одного поста."""
    pid = post.get('id', '?')
    date = post.get('date', '?')
    time = post.get('time', '?')
    text = post.get('text', '')
    photo = post.get('photo')
    photos = post.get('photos')
    title = post.get('title', '')

    # Image src — с веб-префиксом для локального preview
    img_html = ''
    if photos and isinstance(photos, list) and len(photos) > 0:
        # Album — show first
        first = photos[0]
        if first.startswith('http'):
            src = first
        else:
            src = '../../' + first  # relative from drafts/ folder
        img_html = f'<div class="img"><img src="{src}" loading="lazy"><div class="ov">📸 Альбом ({len(photos)} фото)</div></div>'
    elif photo:
        if photo.startswith('http'):
            src = photo
        else:
            src = '../../' + photo  # relative path
        img_html = f'<div class="img"><img src="{src}" loading="lazy"><div class="ov">{html_escape(title[:60])}</div></div>'

    # Date label
    date_label = format_date(date)

    return f'''
<div class="tg">
  <span class="day">{date_label} · {time}</span><span class="pn">#{idx} · {pid}</span>
  <div class="msg">
    {img_html}
    <div class="bd">{text}</div>
    <div class="ft"><span>{time}</span><span>👁 ~?</span></div>
  </div>
</div>
'''


def generate(schedule_filename: str, output_filename: str = None):
    schedule_path = SCHEDULE_DIR / schedule_filename
    if not schedule_path.exists():
        print(f"❌ Schedule not found: {schedule_path}")
        return

    with open(schedule_path, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    week = schedule.get("week", schedule_filename)
    posts = schedule.get("posts", [])
    approved = schedule.get("approved", False)
    notes = schedule.get("_notes", "")

    # Group by date
    posts_by_date = {}
    for post in posts:
        d = post.get("date", "?")
        posts_by_date.setdefault(d, []).append(post)

    # Render
    html_parts = []
    idx = 0
    for date in sorted(posts_by_date.keys()):
        date_posts = posts_by_date[date]
        date_label = format_date(date)
        html_parts.append(f'<div class="day-banner">📅 {date_label} — {len(date_posts)} пост(ов)</div>')
        for post in sorted(date_posts, key=lambda p: p.get("time", "")):
            idx += 1
            html_parts.append(render_post(post, idx))

    posts_html = "\n".join(html_parts)

    status_badge = "✅ APPROVED" if approved else "⏸ DRAFT"

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Превью {week}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, 'Segoe UI', Roboto, sans-serif; background: #0e1621; color: #fff; padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 20px; }}
  h1 {{ color: #aaa; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; margin: 16px 0 0; }}
  .note {{ color: #F6AD55; font-size: 13px; max-width: 460px; text-align: center; background: rgba(246,173,85,0.1); border: 1px solid rgba(246,173,85,0.2); border-radius: 8px; padding: 10px; }}
  .day-banner {{ width: 420px; max-width: 95vw; background: rgba(91,155,213,0.1); border: 1px solid rgba(91,155,213,0.3); border-radius: 8px; padding: 10px; text-align: center; color: #5b9bd5; font-weight: 700; font-size: 14px; margin-top: 12px; }}
  .tg {{ width: 420px; max-width: 95vw; }}
  .msg {{ background: #182533; border-radius: 12px; border-top-left-radius: 4px; overflow: hidden; margin-bottom: 12px; }}
  .img {{ position: relative; width: 100%; height: 220px; overflow: hidden; background: #0a0f15; }}
  .img img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .img .ov {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 8px 12px; background: linear-gradient(transparent, rgba(0,0,0,0.85)); font-size: 11px; color: rgba(255,255,255,0.95); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
  .bd {{ padding: 12px 14px 8px; font-size: 14px; line-height: 1.5; color: #e4e6ea; white-space: pre-wrap; word-wrap: break-word; }}
  .bd b {{ color: #fff; }}
  .bd a {{ color: #5b9bd5; text-decoration: none; }}
  .bd i {{ color: #8dabc4; font-style: italic; }}
  .ft {{ display: flex; justify-content: space-between; padding: 4px 14px 10px; font-size: 11px; color: #708499; }}
  .day {{ color: #F6AD55; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; background: rgba(246,173,85,0.1); border-radius: 4px; padding: 4px 10px; margin-bottom: 8px; display: inline-block; }}
  .pn {{ font-size: 10px; color: #556; float: right; margin-top: 4px; }}
</style>
</head>
<body>

<h1>Превью @afishaCB — {week}</h1>
<div class="note">{status_badge} · {len(posts)} постов · Автогенерация из {schedule_filename}<br>{notes}</div>

{posts_html}

<div style="height: 80px; text-align: center; color: #556; font-size: 11px; padding-top: 16px;">
  Сгенерировано из {schedule_filename}
</div>

</body>
</html>
'''

    if output_filename is None:
        output_filename = schedule_filename.replace(".json", ".html").replace("schedule", "preview")
        if not output_filename.startswith("preview-"):
            output_filename = "preview-" + output_filename
    output_path = DRAFTS_DIR / output_filename

    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Preview generated: {output_path}")
    print(f"   Posts: {len(posts)}")
    print(f"   Status: {status_badge}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_preview.py <schedule-file.json> [--output filename.html]")
        print("Example: python scripts/generate_preview.py week3-apr-13-19.json")
        sys.exit(1)

    schedule_file = sys.argv[1]
    output_file = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output") + 1
        output_file = sys.argv[idx]

    generate(schedule_file, output_file)
