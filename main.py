import threading
import engine
import bot
import payments

print("🚀 SAAS POKÉMON INICIANDO")

threading.Thread(target=engine.start, daemon=True).start()
threading.Thread(target=payments.start, daemon=True).start()

bot.run_bot()