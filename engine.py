import time

from sources.pokemon_api import search_cards
from access import add_alert

SEARCHES = [
    "charizard",
    "umbreon",
    "pikachu",
    "rayquaza",
    "gengar"
]

sent = set()


def calculate_score(card):

    score = 0

    name = card["name"].lower()

    price = card["price"]

    rarity = str(card.get("rarity", "")).lower()

    # preço
    if price < 100:
        score += 20

    if price < 50:
        score += 30

    # raridade
    rare_keywords = [
        "ultra",
        "secret",
        "illustration",
        "full",
        "hyper"
    ]

    for k in rare_keywords:
        if k in rarity:
            score += 25

    # pokémons populares
    hot = [
        "charizard",
        "umbreon",
        "rayquaza",
        "pikachu",
        "gengar"
    ]

    for h in hot:
        if h in name:
            score += 20

    return score


def start():

    print("📡 ENGINE GLOBAL ONLINE")

    while True:

        try:

            for q in SEARCHES:

                print(f"🔍 Buscando {q}")

                cards = search_cards(q)

                print(f"📦 {len(cards)} encontrados")

                for c in cards:

                    score = calculate_score(c)

                    if score < 40:
                        continue

                    key = f"{c['name']}-{c['price']}"

                    if key in sent:
                        continue

                    sent.add(key)

                    c["score"] = score

                    print(
                        f"🔥 ALERTA: {c['name']} | ${c['price']}"
                    )

                    add_alert(c)

            time.sleep(60)

        except Exception as e:

            print("❌ ERRO ENGINE:", e)

            time.sleep(15)