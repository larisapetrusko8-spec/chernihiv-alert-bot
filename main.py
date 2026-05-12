from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import os
import random
import requests

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SESSION_STRING = os.getenv("SESSION_STRING")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

SOURCE_CHANNELS = ["chernihiv_nebo", "Northern_Sich_ukr"]

CHERNIHIV_KEYWORDS = [
    "черніг",
    "черниг",
    "ніжин",
    "нежин",
    "прилук",
    "прилуки",
    "корюк",
    "новгород",
    "сіверськ",
    "сновськ",
    "бахмач",
    "мена",
    "носів",
    "городня",
    "козеле",
    "бобровиц",
    "ріпк",
    "семенів",
]

SIGNATURE = (
    '\n\n🍅 <a href="https://t.me/pomidorpochernihivski">Помідор по-чернігівськи</a> | '
    '<a href="https://t.me/pomidoradmin">Надіслати новину</a>'
)

ENDING_PHRASES = [
    "Слідкуємо за ситуацією",
    "Деталі уточнюються",
    "Бережіть себе",
    "Інформація оновлюється"
]

def is_chernihiv_related(text):
    text = text.lower()
    return any(word in text for word in CHERNIHIV_KEYWORDS)

def rewrite_text(text):
    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if "http://" in line or "https://" in line or "t.me/" in line:
            continue

        lines.append(line)

    rewritten = "\n".join(lines)

    rewritten = rewritten.replace("Увага", "⚠️ Увага")
    rewritten = rewritten.replace("Повітряна тривога", "🚨 Повітряна тривога")
    rewritten = rewritten.replace("БпЛА", "🛸 БпЛА")
    rewritten = rewritten.replace("Шахед", "🛸 Шахед")
    rewritten = rewritten.replace("ракета", "🚀 ракета")

    rewritten += f"\n\n{random.choice(ENDING_PHRASES)}"

    return rewritten

def send_to_channel(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    })

    print(response.text)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    text = event.raw_text

    if not text:
        return

    if not is_chernihiv_related(text):
        return

    final_message = rewrite_text(text) + SIGNATURE
    send_to_channel(final_message)

async def main():
    print("Chernihiv alert monitor started", flush=True)

    if not SESSION_STRING:
        print("ERROR: SESSION_STRING missing", flush=True)
        return

    await client.connect()

    if not await client.is_user_authorized():
        print("ERROR: Invalid SESSION_STRING", flush=True)
        return

    print("Telegram session authorized", flush=True)

    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        text = event.raw_text.lower()

        if any(keyword in text for keyword in CHERNIHIV_KEYWORDS):
            print("Matched news:", event.raw_text[:100], flush=True)

            rewritten = rewrite_news(event.raw_text)

            final_text = f"{rewritten}\n\n{SIGNATURE}"

            await client.send_message(
                entity=int(CHANNEL_ID),
                message=final_text,
                parse_mode="html",
                link_preview=False
            )

            print("News forwarded", flush=True)

    await client.run_until_disconnected()


asyncio.run(main())