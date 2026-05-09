import time
from pokemon_api import get_cards
from db import save_price, get_average_price
from analyzer import calculate_score
from bot import send_alert

print("🚀 MONITOR POKEMON INICIADO")

# =========================
# CONFIG
# =========================

cards_to_track = [
    "charizard",
    "umbreon",
    "rayquaza",
    "gengar",
    "pikachu",
]

# anti-spam
last_alerts = {}

# cooldown em segundos
COOLDOWN = 3600  # 1 hora

# =========================
# LOOP PRINCIPAL
# =========================

while True:

    print("📡 MONITORANDO MERCADO...")

    try:

        for query in cards_to_track:

            cards = get_cards(query)

            if not cards:
                continue

            for card in cards[:3]:

                try:

                    name = card["name"]

                    set_name = card["set"]["name"]

                    number = card["number"]

                    image = card["images"]["large"]

                    prices = card.get("tcgplayer", {}).get("prices", {})

                    market_price = None

                    # tenta pegar o melhor preço disponível
                    for rarity_type in prices.values():

                        if isinstance(rarity_type, dict):

                            market_price = rarity_type.get("market")

                            if market_price:
                                break

                    if not market_price:
                        continue

                    print(f"{name} - ${market_price}")

                    # salva histórico
                    save_price(name, market_price)

                    # média histórica
                    avg = get_average_price(name)

                    if not avg:
                        continue

                    # calcula score
                    score = calculate_score(
                        market_price,
                        avg
                    )

                    # threshold oportunidade
                    if score > 0.25:

                        now = time.time()

                        # anti-spam
                        if name in last_alerts:

                            elapsed = now - last_alerts[name]

                            if elapsed < COOLDOWN:
                                continue

                        last_alerts[name] = now

                        msg = (
                            f"🔥 OPORTUNIDADE DETECTADA\n\n"
                            f"🃏 {name}\n"
                            f"📦 Coleção: {set_name}\n"
                            f"🔢 Número: {number}\n\n"
                            f"💰 Preço Atual: ${market_price}\n"
                            f"📊 Média Histórica: ${avg:.2f}\n"
                            f"📈 Score: {score:.2f}"
                        )

                        send_alert(
                            msg,
                            image=image
                        )

                        print("✅ ALERTA ENVIADO")

                except Exception as card_error:

                    print("ERRO CARTA:", card_error)

    except Exception as e:

        print("ERRO LOOP:", e)

    # intervalo
    time.sleep(300)