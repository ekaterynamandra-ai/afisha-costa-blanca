"""Publish Week 1 (Semana Santa) - posts #2-#9 from april-full-month.html"""
import os, sys, time, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(text, photo=None):
    if photo:
        r = requests.post(f"{API}/sendPhoto", data={"chat_id": CHANNEL_ID, "photo": photo, "caption": text, "parse_mode": "HTML"})
    else:
        r = requests.post(f"{API}/sendMessage", data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True})
    d = r.json()
    if d.get("ok"):
        print(f"OK")
    else:
        print(f"ERROR: {d.get('description','?')}")
        if photo:
            print("Retry without photo...")
            requests.post(f"{API}/sendMessage", data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True})
    return d

posts = [
    # #2 - Semana Santa overview
    {
        "photo": "https://images.pexels.com/photos/13598504/pexels-photo-13598504.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "text": """🕊️ <b>SEMANA SANTA: где и что смотреть на Costa Blanca</b>

🏆 <b>ОРИХУЭЛА</b> — лучшая! Международный туристический интерес
Скульптуры XVI века. Ночная процессия при свечах. <a href="https://www.google.com/maps/place/Orihuela/">📍 карта</a>

🥈 <b>КРЕЙВИЛЛЕНТ</b> — Национальный интерес
Рассвет Страстной пятницы — «Abrazo de la Morquera». <a href="https://www.google.com/maps/place/Crevillent/">📍 карта</a>

🥉 <b>АЛИКАНТЕ</b> — 28 процессий
Район Санта-Крус — самый атмосферный. <a href="https://www.google.com/maps/place/Barrio+Santa+Cruz,+Alicante/">📍 карта</a>

📍 <b>ГУАРДАМАР</b> — живой театр! Пт 3 апр 20:30
📍 <b>ТОРРЕВЬЕХА</b> — новый маршрут 2026
📍 <b>ЭЛЬЧЕ</b> — юбилей 325 лет!

💡 <b>Совет:</b> Самое зрелищное — Страстная пятница (3 апреля). Орихуэла стоит поездки!

🎯 <b>Подойдёт:</b> 👨‍👩‍👧 семьям · 💑 парам · 📸 фотографам

#SemanaSanta #CostaBlanca #Орихуэла #Пасха"""
    },
    # #3 - Orihuela accent
    {
        "photo": "https://images.pexels.com/photos/31715517/pexels-photo-31715517.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "text": """🏆 <b>ОРИХУЭЛА: лучшая Semana Santa на Costa Blanca</b>

Уровень Севильи! Единственная с титулом «Международный туристический интерес».

<b>Расписание:</b>
📅 <b>Пт 3 апр, 19:15</b> — «Convocatoria» (десятки колоколов!)
📅 <b>Пт 3 апр, 01:00</b> — Ночная процессия при свечах 🕯️
📅 <b>Сб 4 апр, 20:15</b> — «Santo Entierro», стиль XVIII века

📍 <a href="https://www.google.com/maps/place/Orihuela/">Орихуэла</a> (30 мин от Торревьехи) · 💰 Бесплатно

💡 <b>Совет:</b> Приезжайте за час. Лучшие точки — Plaza de las Salesas. Ночная в 1:00 — оденьтесь тепло!

🎯 💑 парам · 📸 фотографам · 👨‍👩‍👧 семьям (днём)

#SemanaSanta #Орихуэла #CostaBlanca"""
    },
    # #4 - Markets
    {
        "photo": None,
        "text": """🛍️ <b>РЫНКИ: расписание на апрель</b>

📅 <b>Пн</b> — <a href="https://www.google.com/maps/place/Santa+Pola/">Санта-Пола</a> (~450)
📅 <b>Вт</b> — <a href="https://www.google.com/maps/place/Orihuela/">Орихуэла</a> (~400, продукты с уэрт!)
📅 <b>Ср</b> — <a href="https://www.google.com/maps/place/Guardamar+del+Segura/">Гуардамар</a> · Бенидорм
📅 <b>Чт</b> — <a href="https://www.google.com/maps/place/Alicante/">Аликанте</a> (~375)
📅 <b>Пт</b> — <b>ТОРРЕВЬЕХА</b> 🔥 500+! 8:00-14:00
📅 <b>Сб</b> — Санта-Пола · Аликанте
📅 <b>Вс</b> — <b>El Campico</b> 🔥 ~500! 8:00-15:00

💡 Работают в дождь и в праздники!

📱 <b>@afishaCB</b>

#рынки #mercadillo #CostaBlanca"""
    },
    # #5 - Medieval market Santa Pola
    {
        "photo": None,
        "text": """🏰 <b>2-6 АПРЕЛЯ: Средневековый рынок у крепости Санта-Пола</b>

У стен крепости XVI века — средневековый рынок с традиционной едой (arroz a banda, паэлья), ремесленные лавки, уличные артисты.

📅 2-6 апреля
📍 <a href="https://www.google.com/maps/place/Castillo+Fortaleza+de+Santa+Pola/">Castillo Fortaleza de Santa Pola</a> (15 мин)
💰 Вход бесплатный

🎯 👨‍👩‍👧 семьям · 🍽️ гурманам · 📸 фотографам

#СантаПола #средневековье #CostaBlanca"""
    },
    # #6 - Easter weekend picks
    {
        "photo": None,
        "text": """🌟 <b>ПАСХАЛЬНЫЕ ВЫХОДНЫЕ 4-6 АПРЕЛЯ: куда пойти</b>

1️⃣ 🕊️ <b>Semana Santa — финальные процессии</b>
Пт вечер → Вс утро. Орихуэла, Гуардамар, Торревьеха
→ <i>Парам, семьям, фотографам</i>

2️⃣ 🏰 <b>Средневековый рынок — Санта-Пола</b> <a href="https://www.google.com/maps/place/Castillo+Fortaleza+de+Santa+Pola/">📍</a>
Сб-Вс · Бесплатно · Еда, ремёсла, артисты
→ <i>С детьми, гурманам</i>

3️⃣ 🎨 <b>RODEARTE — арт-рынок в пещерах</b> <a href="https://www.google.com/maps/place/Cuevas+del+Rodeo,+Rojales/">📍</a>
Вс 5 апр 10:00-15:00 · Бесплатно · В пещерах!
→ <i>С подружками, парам, с детьми</i>

4️⃣ 🦩 <b>Фламинго — пик сезона!</b> <a href="https://www.google.com/maps/place/Parque+Natural+de+las+Salinas+de+Santa+Pola/">📍</a>
Любой день · Бесплатно · До 8000 птиц
→ <i>С собакой, всем</i>

📱 <b>@afishaCB</b> — подборки каждую среду!

#Пасха #выходные #CostaBlanca"""
    },
    # #7 - Dogs
    {
        "photo": "https://images.pexels.com/photos/2253275/pexels-photo-2253275.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "text": """🐕 <b>С СОБАКОЙ: лучшие пляжи и маршруты</b>

Апрель — идеально: тепло, пляжи пустые.

🏖️ <b>Playa Los Tusales</b> <a href="https://www.google.com/maps/place/Playa+de+Los+Tusales/">📍</a>
Гуардамар · Песчаный, у дюн

🏖️ <b>Cala Ferrís</b> <a href="https://www.google.com/maps/place/Cala+Ferris,+Torrevieja/">📍</a>
Торревьеха · Аджилити + душ!

🏖️ <b>Caleta dels Gossets</b> <a href="https://www.google.com/maps/place/Caleta+dels+Gossets/">📍</a>
Санта-Пола · Бухта у скал

🌲 <b>Парк Альфонсо XIII</b> <a href="https://www.google.com/maps/place/Parque+Alfonso+XIII,+Guardamar+del+Segura/">📍</a>
Гуардамар · 800 га тени

🦩 <b>Лагуна Ла-Мата</b> <a href="https://www.google.com/maps/place/Parque+Natural+de+las+Lagunas+de+La+Mata+y+Torrevieja/">📍</a>
Торревьеха · Фламинго!

💡 В апреле собачьи пляжи свободны — лучшее время!

#ссобакой #CostaBlanca #собачийпляж"""
    },
    # #8 - Good Friday
    {
        "photo": None,
        "text": """🔴 <b>СЕГОДНЯ ВЫХОДНОЙ: Страстная пятница</b>

Магазины закрыты. Рестораны работают. Рынки — тоже! 🛍️

🕊️ <b>Процессии сегодня:</b>
· Орихуэла 19:15 + 01:00 ночь
· Гуардамар 20:30
· Торревьеха — весь день
· Аликанте — Santo Entierro

💡 Лучший вечер для процессий — сегодня!

#SemanaSanta #CostaBlanca #ВиернесСанто"""
    },
    # #9 - RODEARTE
    {
        "photo": None,
        "text": """🎨 <b>ЗАВТРА: RODEARTE — арт-рынок в пещерах Рохалеса</b>

20+ ремесленных лавок в подземных пещерах! Керамика, ювелирка, мастер-классы, живая музыка. + «Swap Party» — обмен одеждой.

📅 Вс 5 апреля, 10:00-15:00
📍 <a href="https://www.google.com/maps/place/Cuevas+del+Rodeo,+Rojales/">Cuevas del Rodeo, Рохалес</a> (15 мин)
💰 Бесплатно

🎯 👯‍♀️ с подружками · 💑 парам · 👨‍👩‍👧 с детьми

📱 <b>@afishaCB</b>

#RODEARTE #Рохалес #CostaBlanca"""
    },
]

print(f"Publishing Week 1: {len(posts)} posts to {CHANNEL_ID}...")
for i, p in enumerate(posts):
    print(f"\n--- Post {i+1}/{len(posts)} ---")
    send(p["text"], p.get("photo"))
    if i < len(posts) - 1:
        time.sleep(4)
print(f"\nDone! Week 1 published.")
