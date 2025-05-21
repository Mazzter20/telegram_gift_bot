# telegram_gift_bot.py
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from filters import is_good_deal, update_user_filters
from storage import load_seen_ids, save_seen_ids, load_price_history, update_price_history
import asyncio
import logging

# --- CONFIG ---
api_id = 12345678  # Заміни на свій
api_hash = 'your_api_hash'  # Заміни на свій
session_name = 'gift_watcher'
channel_username = 'Tonnel_Network_bot'

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

seen_gifts = load_seen_ids()
price_history = load_price_history()
user_filters = {
    'keywords': ['iPhone', 'AirPods'],
    'max_price': None,
    'min_discount': 10  # %
}

async def ask_user_preferences():
    print("🔧 Введіть ваші побажання щодо подарунків:")
    keywords = input("Ключові слова (через кому): ").split(',')
    try:
        max_price = float(input("Максимальна ціна (залиште порожнім, якщо не важливо): ") or 0)
    except ValueError:
        max_price = None
    try:
        min_discount = float(input("Мінімальна знижка у % від останніх продажів: "))
    except ValueError:
        min_discount = 10

    update_user_filters(user_filters, keywords, max_price, min_discount)

async def check_for_deals(client):
    global seen_gifts, price_history

    result = await client(GetHistoryRequest(
        peer=channel_username,
        limit=20,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    for message in result.messages:
        if message.id in seen_gifts:
            continue
        seen_gifts.add(message.id)

        if is_good_deal(message, price_history, user_filters):
            print(f"🎁 Знайдено вигідну пропозицію: {message.message}")
        update_price_history(price_history, message)

    save_seen_ids(seen_gifts)

async def main():
    await ask_user_preferences()

    async with TelegramClient(session_name, api_id, api_hash) as client:
        print("✅ Підключено. Сканую подарунки...")
        while True:
            try:
                await check_for_deals(client)
            except Exception as e:
                logger.error(f"Помилка під час перевірки: {e}")
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
