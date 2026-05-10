import threading
import bot
import engine

print("🚀 SISTEMA MONITOR POKÉMON INICIANDO")

# =========================
# ENGINE (BACKGROUND)
# =========================
def run_engine():
    try:
        engine.start()
    except Exception as e:
        print("❌ ERRO ENGINE:", e)

# =========================
# BOT (MAIN THREAD)
# =========================
def run_bot():
    try:
        bot.run_bot()
    except Exception as e:
        print("❌ ERRO BOT:", e)

if __name__ == "__main__":
    threading.Thread(target=run_engine, daemon=True).start()
    run_bot()