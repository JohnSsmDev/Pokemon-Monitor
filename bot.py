import os
from dotenv import load_dotenv
from payments import create_pix_payment
from sources.pokemon_api import search_cards
from watchlist import add_card, get_cards
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from access import is_vip

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# =========================
# START
# =========================
async def start(update, context):

    text = (
        "🔥 RADAR POKÉMON TCG\n\n"
        "Encontre oportunidades de compra "
        "antes do mercado.\n\n"

        "⚡ Recursos:\n"
        "• Alertas automáticos\n"
        "• Busca inteligente\n"
        "• Cartas raras\n"
        "• Oportunidades VIP\n\n"

        "🔎 Comandos:\n"
        "/find charizard\n"
        "/alerts\n"
        "/vip\n"
        "/plans"
    )

    await update.message.reply_text(text)


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

        data = []

        if not data:
            await update.message.reply_text(
                "⚠️ Nenhuma oportunidade encontrada ainda."
            )
            return

        msg = "🔥 OPORTUNIDADES:\n\n"

        for c in data[-10:]:

            msg += (
    f"🔥 {c['name']}\n"
    f"💰 ${c['price']}\n"
    f"🏆 {c.get('rarity')}\n"
    f"📦 {c.get('set')}\n"
    f"⭐ Opportunity Score: {c['score']}/100\n\n"
)

        await update.message.reply_text(msg)

    except Exception as e:
        print("ERRO ALERTS:", e)

        await update.message.reply_text(
            "❌ Erro interno no /alerts"
        )

async def plans(update, context):

    text = (
        "💎 PLANOS RADAR VIP\n\n"

        "🥉 FREE\n"
        "• Busca básica\n"
        "• 5 resultados\n\n"

        "🥇 VIP — R$19,90/mês\n"
        "• Alertas automáticos\n"
        "• Oportunidades raras\n"
        "• Watchlist\n"
        "• Prioridade\n\n"

        "🚀 Assine:\n"
        "/vip"
    )

async def help_cmd(update, context):

    text = (
        "📚 AJUDA\n\n"

        "/find nome\n"
        "Busca cartas\n\n"

        "/find 125/094\n"
        "Busca por número\n\n"

        "/alerts\n"
        "Radar VIP\n\n"

        "/watchlist\n"
        "Lista pessoal\n\n"

        "/vip\n"
        "Assinar VIP"
    )

    await update.message.reply_text(text)

    await update.message.reply_text(text)

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

    items = get_cards(user)

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

    add_card(user, query)

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
    f"🃏 {c['name']}\n\n"
    f"🔢 {c['number']}\n"
    f"🏆 {c['rarity']}\n"
    f"📦 {c['set']}\n"
    f"💰 ${c['price']}\n\n"
    f"⭐ Opportunity Score: {score}/100"
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
    app.add_handler(CommandHandler("plans", plans))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("watchlist", watchlist))

    print("🤖 BOT ONLINE")

    app.run_polling()