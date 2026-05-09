from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from pokemon_api import get_cards
from analyzer import calculate_score
from db import save_price, get_average_price

import os

TOKEN = os.getenv("TOKEN")

print("🚀 BOT INTERATIVO INICIADO")

# =========================
# /start
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    msg = (
        "🔥 Pokemon Market Bot ONLINE\n\n"
        "Use:\n"
        "/card nome_da_carta\n\n"
        "Exemplo:\n"
        "/card umbreon vmax"
    )

    await update.message.reply_text(msg)

# =========================
# /card
# =========================

async def card(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        query = " ".join(context.args)

        if not query:

            await update.message.reply_text(
                "Digite o nome da carta.\n\n"
                "Exemplo:\n"
                "/card charizard"
            )

            return

        cards = get_cards(query)

        if not cards:

            await update.message.reply_text(
                "Carta não encontrada."
            )

            return

        card_data = cards[0]

        name = card_data["name"]

        set_name = card_data["set"]["name"]

        number = card_data["number"]

        rarity = card_data.get(
            "rarity",
            "Desconhecida"
        )

        image = card_data["images"]["large"]

        prices = card_data.get(
            "tcgplayer",
            {}
        ).get(
            "prices",
            {}
        )

        market_price = None

        for p in prices.values():

            if isinstance(p, dict):

                market_price = p.get("market")

                if market_price:
                    break

        if not market_price:

            await update.message.reply_text(
                "Sem preço disponível."
            )

            return

        # salva histórico
        save_price(
            name,
            market_price
        )

        # média histórica
        avg = get_average_price(name)

        if not avg:
            avg = market_price

        # score
        score = calculate_score(
            market_price,
            avg
        )

        msg = (
            f"🃏 {name}\n\n"
            f"📦 Coleção: {set_name}\n"
            f"🔢 Número: {number}\n"
            f"⭐ Raridade: {rarity}\n\n"
            f"💰 Market Price: ${market_price}\n"
            f"📊 Média: ${avg:.2f}\n"
            f"🔥 Score: {score:.2f}"
        )

        await update.message.reply_photo(
            photo=image,
            caption=msg
        )

        print(f"CONSULTA: {query}")

    except Exception as e:

        print("ERRO:", e)

        await update.message.reply_text(
            "Erro ao consultar carta."
        )

# =========================
# APP
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("card", card)
)

print("✅ BOT ONLINE")

app.run_polling()