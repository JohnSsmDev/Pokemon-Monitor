import os
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def send_alert(msg, image=None):

    try:

        if image:

            bot.send_photo(
                chat_id=CHAT_ID,
                photo=image,
                caption=msg
            )

        else:

            bot.send_message(
                chat_id=CHAT_ID,
                text=msg
            )

        print("ALERTA ENVIADO")

    except Exception as e:

        print("ERRO TELEGRAM:", e)