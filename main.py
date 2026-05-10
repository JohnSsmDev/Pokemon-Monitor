import threading

import bot
import engine

print("🚀 SAAS POKÉMON INICIANDO")

threading.Thread(
    target=engine.run_engine,
    daemon=True
).start()

bot.run_bot()