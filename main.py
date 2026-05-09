from telegram.ext import Updater, CommandHandler
from pokemon_api import get_cards
from analyzer import calculate_score
from db import save_price, get_average_price
import os

TOKEN = os.getenv("TOKEN")

print("🚀 BOT INTERATIVO INICIADO")

# =========================
# /start
# =========================

def start(update, context):

    msg = (
        "🔥 Pokemon Market Bot ONLINE\n\n"
        "Use:\n"
        "/card nome_da_carta\n\n"
        "Exemplo:\n"
        "/card umbreon vmax"
    )

    update.message.reply_text(msg)

# =========================
# /card
# =========================

def card(update, context):

    try:

        query = " ".join(context.args)

        if not query:

            update.message.reply_text(
                "Digite o nome da carta.\n\nExemplo:\n/card charizard"
            )

            return

        cards = get_cards(query)

        if not cards:

            update.message.reply_text(
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

            update.message.reply_text(
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

        update.message.reply_photo(
            photo=image,
            caption=msg
        )

        print(f"CONSULTA: {query}")

    except Exception as e:

        print("ERRO:", e)

        update.message.reply_text(
            "Erro ao consultar carta."
        )

# =========================
# TELEGRAM
# =========================

updater = Updater(TOKEN)

dp = updater.dispatcher

dp.add_handler(
    CommandHandler("start", start)
)

dp.add_handler(
    CommandHandler("card", card)
)

# =========================
# START BOT
# =========================

print("✅ BOT ONLINE")

updater.start_polling()

updater.idle()