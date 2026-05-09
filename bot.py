import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

async def send_async(msg, image=None):

    try:

        if image:

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=image,
                caption=msg
            )

        else:

            await bot.send_message(
                chat_id=CHAT_ID,
                text=msg
            )

        print("ALERTA ENVIADO")

    except Exception as e:

        print("ERRO TELEGRAM:", e)

def send_alert(msg, image=None):

    asyncio.run(
        send_async(msg, image)
    )