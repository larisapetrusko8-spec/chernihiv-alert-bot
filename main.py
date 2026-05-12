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
    "менa",
    "мена",
    "бахмач",
    "корюківка",
    "сновськ",
    "семенівка",
    "городня",
    "ріпки",
    "козелець",
    "бобровиця",
]

DANGER_KEYWORDS = [
    "бпла",
    "шахед",
    "шахеди",
    "ракета",
    "ракети",
    "ракетна",
    "пуск",
    "пуски",
    "каб",
    "вибух",
    "вибухи",
    "загроза",
    "небезпека",
    "курс",
    "напрямок",
    "летить",
    "рух"
]

templates = [
    "⚠️ Увага, Чернігів\n\nЄ повідомлення про повітряну загрозу для міста/області\n\nБережіть себе",
    "🚨 Чернігівщина, уважно\n\nФіксується можлива повітряна небезпека\n\nНе ігноруйте тривогу",
    "⚠️ Загроза для Чернігова та області\n\nСлідкуємо за ситуацією",
    "🚨 Чернігів / область\n\nМожлива небезпека в повітрі\n\nКраще бути в безпечному місці",
    "⚠️ Чернігівщина під увагою\n\nЄ ризик повітряної загрози\n\nТримаємося",
]

sent_messages = set()

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    original_text = event.raw_text.lower()

    has_chernihiv = any(word in original_text for word in CHERNIHIV_KEYWORDS)
    has_danger = any(word in original_text for word in DANGER_KEYWORDS)

    if has_chernihiv and has_danger:
        message_key = original_text[:120]

        if message_key in sent_messages:
            return

        sent_messages.add(message_key)

        message = random.choice(templates)

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=message
        )

async def main():
    await client.start()
    print("Chernihiv alert monitor started")
    await client.run_until_disconnected()

asyncio.run(main())