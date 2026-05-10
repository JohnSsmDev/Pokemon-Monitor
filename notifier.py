import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)


async def send_alert(user_id, text, image=None):

    try:

        if image:

            await bot.send_photo(
                chat_id=user_id,
                photo=image,
                caption=text
            )

        else:

            await bot.send_message(
                chat_id=user_id,
                text=text
            )

    except Exception as e:
        print("ERRO ALERTA:", e)