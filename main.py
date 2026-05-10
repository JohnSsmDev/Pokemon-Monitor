import threading
import bot
import engine

# =========================
# BOT THREAD
# =========================
def run_bot():
    try:
        bot.run_bot()
    except Exception as e:
        print("❌ ERRO BOT:", e)

# =========================
# ENGINE THREAD
# =========================
def run_engine():
    try:
        engine.start()
    except Exception as e:
        print("❌ ERRO ENGINE:", e)

# =========================
# START SYSTEM
# =========================
if __name__ == "__main__":
    print("🚀 SISTEMA MONITOR POKÉMON INICIANDO")

    # Engine roda em background
    t1 = threading.Thread(target=run_engine, daemon=True)
    t1.start()

    # Bot roda no thread principal (polling precisa disso)
    run_bot()