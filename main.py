import time

from market_data import get_card_data
from db import save_price, get_history
from analyzer import analyze
from bot import send_alert

# =========================
# ANTI-SPAM
# =========================
last_alert = {}

COOLDOWN = 3600

# =========================
# CARTAS
# =========================
cards_to_track = [
    "Umbreon",
    "Charizard",
    "Rayquaza",
    "Gengar",
    "Pikachu"
]

# =========================
# LOOP
# =========================
while True:

    print("\nMONITORANDO MERCADO...")

    opportunities = []

    for name in cards_to_track:

        data = get_card_data(name)

        if not data:
            continue

        current_price = data["price"]

        if not current_price:
            continue

        save_price(name, current_price)

        history = get_history(name)

        result = analyze(history, current_price)

        if not result:
            continue

        score = result["score"]
        mean = result["mean"]

        opportunities.append(
            (
                score,
                name,
                current_price,
                mean,
                data
            )
        )

    # =========================
    # RANKING
    # =========================
    opportunities.sort(reverse=True)

    print("\nTOP OPORTUNIDADES:")

    for o in opportunities:
        print(o)

    # =========================
    # MELHOR OPORTUNIDADE
    # =========================
    if opportunities:

        top = opportunities[0]

        score, name, price, mean, data = top

        if score > 2:

            now = time.time()

            if name in last_alert:

                if now - last_alert[name] < COOLDOWN:
                    continue

            last_alert[name] = now

            msg = (
                f"🔥 OPORTUNIDADE REAL\n\n"
                f"{data['name']} ({data['number']})\n"
                f"Coleção: {data['set']}\n"
                f"Preço: ${price}\n"
                f"Média: ${mean:.2f}\n"
                f"Score: {score:.2f}"
            )

            send_alert(
                msg,
                data["image"]
            )

    time.sleep(30)