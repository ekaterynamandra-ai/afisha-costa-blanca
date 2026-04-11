"""
Скрипт для скачивания фото в локальную папку content/photos/places/
с понятным именем (по месту/событию).

Использование:
    python scripts/download_photo.py <URL> <semantic-name>

Пример:
    python scripts/download_photo.py "https://upload.wikimedia.org/.../Altea_Iglesia.JPG" altea-iglesia-blue-domes

Имя автоматически получает .jpg/.png в зависимости от исходника.
Если URL — Wikimedia большое фото, автоматически конвертирует в thumbnail 1280px (Telegram limit).
"""

import sys
import os
import urllib.request
import urllib.parse
from pathlib import Path

PHOTOS_DIR = Path(__file__).parent.parent / "content" / "photos" / "places"
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)


def to_wikimedia_thumbnail(url: str, max_width: int = 1280) -> str:
    """Конвертировать оригинальный Wikimedia URL в thumbnail (для bulk-download)."""
    if "upload.wikimedia.org/wikipedia/commons/" not in url:
        return url
    if "/thumb/" in url:
        return url  # уже thumbnail

    # https://upload.wikimedia.org/wikipedia/commons/X/XY/filename.jpg
    # → https://upload.wikimedia.org/wikipedia/commons/thumb/X/XY/filename.jpg/1280px-filename.jpg
    parts = url.split("/wikipedia/commons/")
    if len(parts) != 2:
        return url

    base = parts[0] + "/wikipedia/commons/thumb/"
    rest = parts[1]
    filename = rest.rsplit("/", 1)[-1]
    return f"{base}{rest}/{max_width}px-{filename}"


def download(url: str, semantic_name: str) -> Path:
    """Скачать фото по URL с понятным именем."""
    # Convert Wikimedia URLs to thumbnail
    download_url = to_wikimedia_thumbnail(url)

    # Get extension
    parsed_path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(parsed_path)[1].lower()
    if not ext or ext not in (".jpg", ".jpeg", ".png", ".webp"):
        ext = ".jpg"

    if not semantic_name.endswith(ext):
        semantic_name = semantic_name + ext

    target = PHOTOS_DIR / semantic_name

    if target.exists():
        size_kb = target.stat().st_size // 1024
        print(f"⏭ {semantic_name} already exists ({size_kb} KB)")
        return target

    headers = {"User-Agent": "CostaBlancaProject/1.0 (ekaterynamandra@gmail.com)"}
    req = urllib.request.Request(download_url, headers=headers)

    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read()

    with open(target, "wb") as f:
        f.write(data)

    size_kb = len(data) // 1024
    print(f"✅ {semantic_name} ({size_kb} KB)")
    return target


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/download_photo.py <URL> <semantic-name>")
        sys.exit(1)

    download(sys.argv[1], sys.argv[2])
