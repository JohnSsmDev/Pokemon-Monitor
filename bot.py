from telegram import Bot

TOKEN = "8168537181:AAHzUUy3_Hl2TsZochT6fJL_J-WRrQXmBOo"
CHAT_ID = 6339790119

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