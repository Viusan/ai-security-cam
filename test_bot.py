import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def send_test_message():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Security cam bot is working")

asyncio.run(send_test_message())