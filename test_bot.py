import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def send_test_message():
    bot = Bot(token=TOKEN)
    with open("test_image.jpg", "rb") as photo:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption="Test alert: object detected"
        )

asyncio.run(send_test_message())