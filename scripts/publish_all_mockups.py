"""Publish all mockup posts to @afishaCB"""
import json, os, sys, time, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(text, photo=None):
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
    if d.get("ok"):
        print(f"OK: sent")
    else:
        print(f"ERROR: {d.get('description','?')}")
        # Retry without photo if photo failed
        if photo:
            print("Retrying without photo...")
            r2 = requests.post(f"{API}/sendMessage", data={
                "chat_id": CHANNEL_ID, "text": text,
                "parse_mode": "HTML", "disable_web_page_preview": True
            })
            d2 = r2.json()
            print(f"{'OK' if d2.get('ok') else 'FAIL'}: {d2.get('description','sent')}")
    return d

# ============ MONTH POSTS (preview-month.html) ============

posts = []

# 1. Monthly digest
posts.append({
    "photo": "https://images.pexels.com/photos/29837765/pexels-photo-29837765.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """📅 <b>АПРЕЛЬ 2026: самое интересное по неделям</b>

<b>НЕДЕЛЯ 1: 30 марта – 6 апреля</b>
🕊️ Semana Santa — процессии во всех городах
🏰 2-6 апр: Средневековый рынок у крепости Санта-Пола
🔴 3 апр — Страстная пятница (выходной)
🔴 6 апр — Пасхальный понедельник (выходной)

<b>НЕДЕЛЯ 2: 7–13 апреля</b>
🎮 11-12 апр: Expo Torrevieja + ComarCON (бесплатно!)
🔴 13 апр — San Vicente Ferrer (выходной)
🦩 Фламинго: пик сезона в Салинас

<b>НЕДЕЛЯ 3: 14–20 апреля</b>
🔴 16 апр — Santa Faz (выходной в Аликанте)
🎵 17 апр: DJ Symphonic + оркестр, Торревьеха

<b>НЕДЕЛЯ 4: 21–27 апреля 🔥</b>
🍽️ 24-25 апр: «A Todo Tren!» — тапас-маршрут Торревьехи!
🎭 25-27 апр: Moros y Cristianos, Алькой — ЮБИЛЕЙ 750 ЛЕТ!

<b>Каждую неделю:</b>
🛍️ Пт — мега-рынок Торревьехи (500+ прилавков)
🛍️ Вс — рынок El Campico, Гуардамар (~500)
🦩 Весь месяц — фламинго в Салинас
🌡️ Погода: +20-24°C, идеально для прогулок

📱 Подпишись <b>@afishaCB</b> — подборки каждую неделю!"""
})

# 2. Flamingos
posts.append({
    "photo": "https://images.pexels.com/photos/1680214/pexels-photo-1680214.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """🦩 <b>ФЛАМИНГО: пик сезона — до 8000 птиц у нас под боком!</b>

Апрель — начало гнездования. Стаи растут с 2000 до 8000! Розовые облака на фоне солёных озёр — зрелище, ради которого сюда едут фотографы со всей Европы.

<b>Где смотреть:</b>

1️⃣ <b>Салинас де Санта-Пола</b> <a href="https://www.google.com/maps/place/Parque+Natural+de+las+Salinas+de+Santa+Pola/">📍 карта</a>
15 мин от Гуардамара. Смотровые вышки, центр интерпретации. Самая большая колония!

2️�� <b>Лагуна Ла-Мата</b> <a href="https://www.google.com/maps/place/Parque+Natural+de+las+Lagunas+de+La+Mata+y+Torrevieja/">📍 карта</a>
10 мин от Торревьехи. Дорожки для прогулок. С собакой можно!

3️⃣ <b>Розовое озеро Торревьехи</b> <a href="https://www.google.com/maps/place/Laguna+Rosa+de+Torrevieja/">📍 к��рта</a>
Розовое от соли + розовые фламинго = двойное чудо. Лучшие фото на закате.

💡 <b>Совет:</b> Раннее утро или закат — птицы активнее, свет красивее. Бинокль делает разницу!

🎯 <b>Подойдёт:</b> 👨‍👩���👧 семьям · 📸 фотографам · 🐕 с собакой · 💑 парам

#фламинго #CostaBlanca #СантаПола #природа #розовоеозеро"""
})

# 3. Expo + ComarCON
posts.append({
    "photo": "https://images.pexels.com/photos/1293120/pexels-photo-1293120.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """🎮 <b>11-12 АПРЕЛЯ: Expo Torrevieja + ComarCON — бесплатно!</b>

Два огромных события в один уикенд!

🏢 <b>Expo Torrevieja</b>
180+ стендов, классические авто и мотоциклы (Вс). 10 000 посетителей.
<a href="https://www.google.com/maps/place/Auditorio+Internacional+de+Torrevieja/">📍 Auditorio Internacional</a>

🎮 <b>ComarCON XII</b>
Аниме, косплей, настолки, K-Pop, турниры, мастер-классы. 6000+ фанатов!
<a href="https://www.google.com/maps/place/Palacio+de+los+Deportes+Infanta+Cristina/">📍 Palacio de los Deportes</a>

📅 Сб-Вс, 11-12 апреля
💰 Вход бесплатный, парковка бесплатная

🎯 <b>Подойдёт:</b> 👨‍👩‍👧 семьям · 🧑‍🤝‍🧑 подросткам · 🎉 компанией

#ExpoTorrevieja #ComarCON #Торревьеха #CostaBlanca"""
})

# 4. Tapas route
posts.append({
    "photo": "https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """🍽️ <b>24-25 АПРЕЛЯ: «A Todo Tren!» — тапас-маршрут по Торревьехе</b>

Бары, рестораны и кафе Торревьехи готовят специальные тапас! Три формата:

🍴 Тапа + напиток — ~3-4€
🍰 Десерт + кофе — ~3-4€
🍹 Коктейль — ~3-4€

Сканируешь QR в каждом заведении — участвуешь в розыгрыше: хамон, телефон и... твой вес в пиве! 🍺

📅 Пт-Сб, 24-25 апреля
📍 Центр Торревьехи (маршрут по участникам)

💡 <b>Совет:</b> Карту участников опубликуют на torreviejagastronomica.com. Начните с вечера пятницы — атмосфернее!

🎯 <b>Подойдёт:</b> 💑 парам · 👯‍♀️ с подружками · 🍽️ гурманам · 🎉 компанией

#тапас #гастро #Торревьеха #CostaBlanca"""
})

# 5. Moros y Cristianos
posts.append({
    "photo": "https://images.pexels.com/photos/13598504/pexels-photo-13598504.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """🎭 <b>25-27 АПРЕЛЯ: Moros y Cristianos в Алькое — юбилей 750 лет!</b>

Самый грандиозный костюмированный праздник Испании. 2026 — юбилейный год!

📅 <b>25 апреля</b> — Парад Христиан 10:30, Парад Мавров 17:00
📅 <b>26 апреля</b> — Процессия реликвии 11:00
📅 <b>27 апреля</b> — Битва (Alardo) 11:00 + 17:30, Появление Св. Георгия 21:30

📍 <a href="https://www.google.com/maps/place/Alcoy,+Alicante/">Алькой</a> (55 мин от Аликанте)
💰 Бесплатно

💡 <b>Совет:</b> Самое зрелищное — парады 25-го. Приезжайте к 10 утра! Парковка на окраине, бесплатные шаттлы. Беруши для детей — залпы оглушительн��е!

🎯 <b>Подойдёт:</b> 👨‍👩‍👧 с��мьям · 📸 фотографам · 🎨 культура · 👥 всем

#MorosYCristianos #Алькой #фестиваль #CostaBlanca"""
})

# 6. Sports
posts.append({
    "photo": None,
    "text": """🏃 <b>АКТИВНЫЙ АПРЕЛЬ: где поиграть и покататься</b>

+22°C, без жары — идеальный сезон для спорта!

<b>🎾 Падель и теннис (муниципальные корты):</b>

<b>Ciudad Deportiva Torrevieja</b> <a href="https://www.google.com/maps/place/Ciudad+Deportiva+de+Torrevieja/">📍</a>
Падель: 6€/30 мин · Теннис: 4€/час · Бронь: 966 111 222

<b>Polideportivo Guardamar</b> <a href="https://www.google.com/maps/place/Polideportivo+Municipal+Guardamar+del+Segura/">📍</a>
Падель + теннис: 4€/час · Бронь: 965 729 014

<b>🚴 Велосипед:</b>

<b>Via Verde de Torrevieja</b> <a href="https://www.google.com/maps/place/V%C3%ADa+Verde+de+Torrevieja/">📍</a>
6.7 км, асфальт, плоская. Старая ж/д → пляж.

<b>🛶 На воде (от 15€/час):</b>

<b>Каяк / SUP</b> <a href="https://www.google.com/maps/place/Torrevieja+Surf+%26+SUP+School/">📍</a>
Каяк: 15€/час. SUP: 15€/час.

💡 Корты бронируйте за день — утренние слоты разбирают быстро!

#спорт #падель #велосипед #CostaBlanca"""
})

# 7. Dunes
posts.append({
    "photo": "https://images.pexels.com/photos/1578750/pexels-photo-1578750.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """🌲 <b>ДЮНЫ ГУАРДАМАРА: 800 га леса прямо у пляжа</b>

В Гуардамаре — один из крупнейших искусственных лесов Европы! В начале 1900-х сосны высадили, чтобы остановить наступающие дюны. Сегодня это 800 га тени, тишины и красоты.

🌡️ <b>Почему в апреле:</b> +22°C, весенние цветы, не жарко. Летом будет +38 — не то.

🌸 <b>Что увидите:</b> Сосны, пальмы, эвкалипты. Весенние полевые цветы. Финикийские раскопки La Fonteta (VIII-VI век до н.э.).

🥾 <b>Маршрут:</b> Круговой ~3 км, лёгкий, тенистый. Из леса можно выйти прямо на пляж!

📍 <a href="https://www.google.com/maps/place/Parque+Alfonso+XIII,+Guardamar+del+Segura/">Парк Альфонсо XIII, Гуардамар</a>
💰 Бесплатно, круглый год

🎯 <b>Подойдёт:</b> 🐕 с собакой · 👨‍👩‍👧 семьям · 💑 парам · 🏃 бегунам · 📸 фотографам

#Гуардамар #дюны #природа #CostaBlanca"""
})

# ============ WEEK-ONLY POSTS (preview-week.html, not in month) ============

# 8. Markets schedule
posts.append({
    "photo": "https://images.pexels.com/photos/868110/pexels-photo-868110.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """🛍️ <b>РЫНКИ COSTA BLANCA: расписание на апрель</b>

Сохраняйте!

📅 <b>Пн</b> — <a href="https://www.google.com/maps/place/Santa+Pola/">Санта-Пола</a> (~450 прилавков)
📅 <b>Вт</b> — <a href="https://www.google.com/maps/place/Orihuela/">Орихуэла</a> (~400, продукты с уэрт!)
📅 <b>Ср</b> — <a href="https://www.google.com/maps/place/Guardamar+del+Segura/">Гуардамар</a> · Бенидорм
📅 <b>Чт</b> — <a href="https://www.google.com/maps/place/Calle+Teulada,+Alicante/">Аликанте</a> (Calle Teulada, ~375)
📅 <b>Пт</b> — <b>ТОРРЕВЬЕХА</b> 🔥 500+ прилавков! Бесплатный автобус. 8:00-14:00
📅 <b>Сб</b> — Санта-Пола (фрукты, цветы) · Аликанте
📅 <b>Вс</b> — <b>Гуардамар El Campico</b> 🔥 ~500 прилавков! 8:00-15:00

💡 Рынки работают в дождь и в праздники!

📱 <b>@afishaCB</b>

#рынки #mercadillo #CostaBlanca #Торревьеха #Гуардамар"""
})

# 9. With kids
posts.append({
    "photo": "https://images.pexels.com/photos/1231365/pexels-photo-1231365.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """👨‍��‍👧 <b>С ДЕТЬМИ: 5 идей на эту неделю</b>

1️⃣ <b>🦩 Фламинго в Салинас</b> <a href="https://www.google.com/maps/place/Parque+Natural+de+las+Salinas+de+Santa+Pola/">📍</a>
Бесплатно · 15 мин от Гуардамара · Дети обожают считать розовых птиц!

2️⃣ <b>🎮 ComarCON</b> <a href="https://www.google.com/maps/place/Palacio+de+los+Deportes+Infanta+Cristina/">📍</a>
Бесплатно · Сб-Вс · Косплей, настолки, аниме

3️⃣ <b>🌲 Дюны Гуардамара</b> <a href="https://www.google.com/maps/place/Parque+Alfonso+XIII,+Guardamar+del+Segura/">📍</a>
Бесплатно · Тенистые тропы, финикийские раскопки

4️⃣ <b>🛍️ Рынок El Campico (Вс)</b> <a href="https://www.google.com/maps/place/Guardamar+del+Segura/">📍</a>
Бесплатно · Дети любят выбирать фрукты!

5️⃣ <b>🏖️ Пляж + мороженое в Торревьехе</b>
Апрель: 22°C, не жарко, без толп

#сдетьми #CostaBlanca #Гуардамар #Торревьеха"""
})

# 10. With girlfriends
posts.append({
    "photo": "https://images.pexels.com/photos/1267696/pexels-photo-1267696.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """👯‍♀️ <b>С ПОДРУЖКАМИ: как провести время</b>

1️⃣ <b>🛍️ Пятничный мега-рынок</b> <a href="https://www.google.com/maps/place/Torrevieja/">📍</a>
Торревьеха · 500+ прилавков · Одежда, аксессуары, сумки

2️⃣ <b>📸 Фотосессия у розового озера</b> <a href="https://www.google.com/maps/place/Laguna+Rosa+de+Torrevieja/">📍</a>
Торревьеха · Бесплатно · Инстаграм-мечта!

3️⃣ <b>🎾 Падель вчетвером</b> <a href="https://www.google.com/maps/place/Ciudad+Deportiva+de+Torrevieja/">📍</a>
Ciudad Deportiva · 6€/30 мин на четверых

4️⃣ <b>🧘 Йога на пляже (Сб утро)</b>
Playa del Cura, Торревьеха · Бесплатные группы

#сподружками #CostaBlanca #Торревьеха"""
})

# 11. With dogs
posts.append({
    "photo": "https://images.pexels.com/photos/2253275/pexels-photo-2253275.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    "text": """🐕 <b>С СОБАКОЙ: лучшие пляжи и маршруты</b>

Апрель — идеально: тепло, пляжи пустые, без ограничений.

<b>Пляжи для собак:</b>

🏖️ <b>Playa Los Tusales</b> <a href="https://www.google.com/maps/place/Playa+de+Los+Tusales/">📍</a>
Гуардамар · Песчаный, рядом с дюнами

🏖️ <b>Cala Ferrís</b> <a href="https://www.google.com/maps/place/Cala+Ferris,+Torrevieja/">📍</a>
Торревьеха · Аджилити-площадка + душ!

🏖️ <b>Caleta dels Gossets</b> <a href="https://www.google.com/maps/place/Caleta+dels+Gossets/">📍</a>
Санта-Пола · Бухта у скал, фотогеничная

<b>Маршруты:</b>

🌲 <b>Парк Альфонсо XIII</b> <a href="https://www.google.com/maps/place/Parque+Alfonso+XIII,+Guardamar+del+Segura/">📍</a>
Гуардамар · 800 га тенистого леса

🦩 <b>Лагуна Ла-Мата</b> <a href="https://www.google.com/maps/place/Parque+Natural+de+las+Lagunas+de+La+Mata+y+Torrevieja/">📍</a>
Торревьеха · Дорожки + фламинго!

💡 В апреле все собачьи пляжи свободны — лучшее время!

#ссобакой #CostaBlanca #собачийпляж"""
})

# 12. Nature routes
posts.append({
    "photo": None,
    "text": """🌿 <b>ПРИРОДА В АПРЕЛЕ: 3 маршрута рядом</b>

🌡️ +22°C, весенние цветы, не жарко — идеальный сезон!

1️⃣ <b>🌲 Дюны Гуардамара</b> <a href="https://www.google.com/maps/place/Parque+Alfonso+XIII,+Guardamar+del+Segura/">📍</a>
800 га леса, весенние цветы, финикийские раскопки. Лёгкий, ~3 км.
→ <i>Семьям, с собакой, вдвоём</i>

2️⃣ <b>🦆 Парк Эль-Ондо</b> <a href="https://www.google.com/maps/place/Parque+Natural+El+Hondo/">📍</a>
Между Эльче и Гуардамаром. Птицы, черепахи, тишина. Бинокль!
→ <i>Фотографам, парам, с детьми</i>

3️⃣ <b>⛰️ Сьерра-де-Эскалона</b> <a href="https://www.google.com/maps/place/Sierra+Escalona/">📍</a>
30 мин от Торревьехи. Горная сосна, виды. Средняя сложность.
→ <i>Активным, с собакой</i>

💡 Берите воду и крем от солнца. Утро — лучшее время для птиц.

#природа #CostaBlanca #походы #Гуардамар"""
})

# ============ PUBLISH ALL ============

print(f"Publishing {len(posts)} posts to {CHANNEL_ID}...")
for i, post in enumerate(posts):
    print(f"\n--- Post {i+1}/{len(posts)} ---")
    send(post["text"], post.get("photo"))
    if i < len(posts) - 1:
        time.sleep(4)

print(f"\nDone! {len(posts)} posts published.")
