import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from Main.Pagamentos.payments import create_payment
from pokemon_api import get_cards
from Main.Bot.analyzer import calculate_score

from db import (
    save_price,
    get_average_price,
    register_user,
    is_vip,
    can_use,
    add_request
)

TOKEN = os.getenv("TOKEN")

print("🚀 BOT ONLINE")


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 POKÉMON BOT\n\n"
        "/card nome ou número\n"
        "/vip ativar assinatura\n\n"
        "Ex:\n"
        "/card Charizard EX\n"
        "/card 215/198\n\n"
        "💎 VIP: ilimitado + análises"
    )


# =========================
# VIP (PIX AUTOMÁTICO)
# =========================
async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    register_user(user_id)

    payment = create_payment(user_id)

    pix = None

    try:
        pix = payment.get("point_of_interaction", {}) \
                     .get("transaction_data", {}) \
                     .get("qr_code")
    except:
        pass

    if not pix:

        await update.message.reply_text(
            "❌ Erro ao gerar PIX. Tente novamente."
        )
        return

    await update.message.reply_text(
        "💎 VIP POKÉMON BOT\n\n"
        "Pagamento via PIX:\n\n"
        f"{pix}\n\n"
        "Após pagamento, liberação automática."
    )


# =========================
# CARD SEARCH
# =========================
async def card(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    register_user(user_id)

    # LIMITE FREE
    if not is_vip(user_id):

        if not can_use(user_id):

            await update.message.reply_text(
                "⚠ Limite diário atingido.\nUse /vip para liberar acesso."
            )
            return

        add_request(user_id)

    query = " ".join(context.args)

    if not query:

        await update.message.reply_text("Digite o nome ou número da carta.")
        return

    cards = get_cards(query)

    if not cards:

        await update.message.reply_text("Carta não encontrada.")
        return

    cards = cards[:5]

    for c in cards:

        try:

            name = c.get("name")
            set_name = c.get("set", {}).get("name")
            number = c.get("number")
            rarity = c.get("rarity", "N/A")
            image = c.get("images", {}).get("large")

            prices = c.get("tcgplayer", {}).get("prices", {})

            market_price = None

            for p in prices.values():
                if isinstance(p, dict):
                    market_price = p.get("market")
                    if market_price:
                        break

            avg = None
            score = None

            if market_price:

                save_price(name, market_price)

                avg = get_average_price(name)

                if avg:
                    score = calculate_score(market_price, avg)

            msg = (
                f"🃏 {name}\n\n"
                f"📦 {set_name}\n"
                f"🔢 {number}\n"
                f"⭐ {rarity}\n\n"
                f"💰 ${market_price if market_price else 'N/A'}\n"
            )

            if avg and score:

                msg += (
                    f"📊 Média: ${avg:.2f}\n"
                    f"🔥 Score: {score:.2f}"
                )

            if image:
                await update.message.reply_photo(image, caption=msg)
            else:
                await update.message.reply_text(msg)

        except Exception as e:
            print("ERRO CARD:", e)


# =========================
# APP
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vip", vip))
app.add_handler(CommandHandler("card", card))

print("✅ BOT RODANDO")

app.run_polling()