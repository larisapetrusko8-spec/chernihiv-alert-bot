from telethon import TelegramClient, events
from telegram import Bot
import asyncio
import os
import random

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

client = TelegramClient("session", API_ID, API_HASH)
bot = Bot(token=BOT_TOKEN)

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
        "ракета": "🚀 ракета",
        "Шахед": "🛸 Шахед"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text += f"\n\n{random.choice(ENDING_PHRASES)}"

    return text

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        text = event.raw_text

        if not text:
            return

        if not is_chernihiv_related(text):
            return

        rewritten_text = rewrite_text(text)

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=rewritten_text + SIGNATURE,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

        print("Новина відправлена")

    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    print("Chernihiv alert monitor started")
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())