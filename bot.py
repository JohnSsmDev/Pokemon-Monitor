import os
from dotenv import load_dotenv
from sources.pokemon_api import search_cards
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

    print("ID USER:", update.effective_user.id)

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
    f"💰 ${c['price']}\n"
    f"⭐ Score: {c['score']}\n"
    f"🏆 {c.get('rarity')}\n"
    f"📦 {c.get('set')}\n\n"
)

        await update.message.reply_text(msg)

    except Exception as e:
        print("ERRO ALERTS:", e)

        await update.message.reply_text(
            "❌ Erro interno no /alerts"
        )

async def find(update, context):

    if not context.args:
        await update.message.reply_text(
            "Use: /find nome_da_carta"
        )
        return

    query = " ".join(context.args)

    await update.message.reply_text(
        f"🔍 Procurando: {query}"
    )

    cards = search_cards(query)

    if not cards:

        await update.message.reply_text(
            "❌ Nenhuma carta encontrada."
        )
        return

    for c in cards[:5]:

        score = 0

        if c["price"] < 100:
            score += 20

        if c["rarity"]:
            rarity = c["rarity"].lower()

            if (
                "secret" in rarity
                or "ultra" in rarity
                or "illustration" in rarity
            ):
                score += 30

        caption = (
            f"🃏 {c['name']}\n"
            f"🔢 {c['number']}\n"
            f"🏆 {c['rarity']}\n"
            f"📦 {c['set']}\n"
            f"💰 ${c['price']}\n"
            f"⭐ Score: {score}"
        )

        await update.message.reply_photo(
            photo=c["image"],
            caption=caption
        )
# =========================
# RUN BOT
# =========================
def run_bot():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("alerts", alerts))
    app.add_handler(CommandHandler("find", find))
    
    print("🤖 BOT ONLINE")

    app.run_polling()