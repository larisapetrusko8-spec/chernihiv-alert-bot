from telethon import TelegramClient, events
import asyncio
import os
import random
import requests

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

from telethon.sessions import StringSession

client = TelegramClient(
    StringSession(os.getenv("SESSION_STRING")),
    API_ID,
    API_HASH
)

SOURCE_CHANNELS = [
    "chernihiv_nebo",
    "Northern_Sich_ukr"
]

CHERNIHIV_KEYWORDS = [
    "чернігів",
    "чернігівщина",
    "чернігівської",
    "чернігівську",
    "чернігівщину",
    "чернігівщини",
    "чернигов",
    "черниговщина",
    "черниговскую",
    "ніжин",
    "нежин",
    "прилуки",
    "новгород-сіверський",
    "новгород сіверський",
    "носівка",
    "мена",
    "бахмач",
    "корюківка",
    "сновськ",
    "семенівка",
    "городня",
    "ріпки",
    "козелець",
    "бобровиця"
]

SIGNATURE = (
    '\n\n🍅 <a href="https://t.me/pomidorpochernihivski">Помідор по-чернігівськи</a> | '
    '<a href="https://t.me/pomidoradmin">Надіслати новину</a>'
)

ENDING_PHRASES = [
    "Ситуація залишається напруженою",
    "Слідкуємо за ситуацією",
    "Деталі уточнюються",
    "Бережіть себе",
    "Тривожна ніч для області",
    "Інформація оновлюється"
]

def is_chernihiv_related(text):
    text = text.lower()
    return any(word in text for word in CHERNIHIV_KEYWORDS)

def rewrite_text(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if "https://" in line or "http://" in line:
            continue

        cleaned.append(line)

    text = "\n".join(cleaned)

    replacements = {
        "Повітряна тривога": "🚨 Повітряна тривога",
        "Увага": "⚠️ Увага",
        "БпЛА": "🛸 БпЛА",
        "Шахед": "🛸 Шахед",
        "шахед": "🛸 шахед",
        "ракета": "🚀 ракета",
        "Ракета": "🚀 Ракета"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text += f"\n\n{random.choice(ENDING_PHRASES)}"

    return text

def send_to_channel(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        print("Telegram send error:", response.text)
    else:
        print("Новина відправлена")

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        text = event.raw_text

        if not text:
            return

        if not is_chernihiv_related(text):
            return

        rewritten_text = rewrite_text(text)
        final_message = rewritten_text + SIGNATURE

        send_to_channel(final_message)

    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    print("Chernihiv alert monitor started")
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())