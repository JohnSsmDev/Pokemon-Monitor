import os
from dotenv import load_dotenv
from payments import create_pix_payment
from sources.pokemon_api import search_cards
from watchlist import add_watch, get_watchs
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

async def vip(update, context):

    user = str(update.effective_user.id)

    payment = create_pix_payment(user)

    msg = (
        "🔥 VIP RADAR POKÉMON\n\n"
        "💰 Plano Mensal: R$19,90\n\n"
        "📲 PIX COPIA E COLA:\n\n"
        f"{payment['pix_code']}"
    )

    await update.message.reply_text(msg)

    await update.message.reply_text(msg)

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

async def watchlist(update, context):

    user = str(update.effective_user.id)

    items = get_watchs(user)

    if not items:

        await update.message.reply_text(
            "❌ Sua watchlist está vazia."
        )
        return

    msg = "👀 SUA WATCHLIST:\n\n"

    for i in items:

        msg += f"• {i}\n"

    await update.message.reply_text(msg)

async def watch(update, context):

    if not context.args:

        await update.message.reply_text(
            "Use: /watch nome_da_carta"
        )
        return

    query = " ".join(context.args)

    user = str(update.effective_user.id)

    add_watch(user, query)

    await update.message.reply_text(
        f"✅ Agora monitorando: {query}"
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
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("watchlist", watchlist))

    print("🤖 BOT ONLINE")

    app.run_polling()