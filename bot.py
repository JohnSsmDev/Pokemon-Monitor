import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# =========================
# HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 BOT ONLINE - Monitor Pokémon ativo!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 pong")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("❌ ERRO BOT:", context.error)

# =========================
# RUN BOT
# =========================
def run_bot():
    if not TOKEN:
        raise ValueError("BOT_TOKEN não encontrado no .env")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_error_handler(error_handler)

    print("🤖 BOT ONLINE")
    app.run_polling(drop_pending_updates=True)