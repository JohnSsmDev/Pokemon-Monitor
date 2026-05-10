import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from access import is_vip, get_alerts

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Radar Pokémon ativo"
    )


# =========================
# ALERTS
# =========================
async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user = str(update.effective_user.id)

        if not is_vip(user):
            await update.message.reply_text(
                "❌ Você não possui VIP ainda."
            )
            return

        data = get_alerts()

        if not data:
            await update.message.reply_text(
                "⚠️ Nenhuma oportunidade encontrada ainda."
            )
            return

        msg = "🔥 OPORTUNIDADES:\n\n"

        for c in data[-10:]:

            msg += (
                f"🃏 {c['name']}\n"
                f"💰 R${c['price']}\n"
                f"⭐ Score: {c['score']}\n\n"
            )

        await update.message.reply_text(msg)

    except Exception as e:
        print("ERRO ALERTS:", e)

        await update.message.reply_text(
            "❌ Erro interno no /alerts"
        )


# =========================
# RUN BOT
# =========================
def run_bot():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("alerts", alerts))

    print("🤖 BOT ONLINE")

    app.run_polling()