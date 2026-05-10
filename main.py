import threading
import bot
import engine

print("🚀 SISTEMA MONITOR POKÉMON INICIANDO")

# engine em background
threading.Thread(target=engine.start, daemon=True).start()

# bot roda no main thread
bot.run_bot()