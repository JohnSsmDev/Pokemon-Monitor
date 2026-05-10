import threading

import bot
import engine
from webhook import app


def run_web():

    app.run(
        host="0.0.0.0",
        port=8080
    )


print("🚀 SAAS POKÉMON INICIANDO")

threading.Thread(
    target=engine.run_engine,
    daemon=True
).start()

threading.Thread(
    target=run_web,
    daemon=True
).start()

bot.run_bot()