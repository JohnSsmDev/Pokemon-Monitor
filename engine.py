import time

from sources.ligapokemon import search_liga
from access import add_alert

SEARCHES = [
    "charizard",
    "umbreon",
    "pikachu",
    "rayquaza",
    "gengar",
]

sent = set()


def calculate_score(card):

    score = 0

    name = card["name"].lower()
    price = card["price"]

    # preço baixo
    if price < 100:
        score += 30

    # muito barato
    if price < 50:
        score += 30

    # pokémons populares
    hot = [
        "charizard",
        "umbreon",
        "pikachu",
        "rayquaza",
        "gengar",
    ]

    for h in hot:
        if h in name:
            score += 25

    # full art / raras
    keywords = [
        "vmax",
        "vstar",
        "gx",
        "ex",
        "full art",
        "illustration",
        "secret"
    ]

    for k in keywords:
        if k in name:
            score += 20

    return score


def start():

    print("📡 ENGINE LIGA POKÉMON ONLINE")

    while True:

        try:

            for q in SEARCHES:

                cards = search_liga(q)

                for c in cards:

                    score = calculate_score(c)

                    if score < 50:
                        continue

                    key = f"{c['name']}-{c['price']}"

                    if key in sent:
                        continue

                    sent.add(key)

                    c["score"] = score

                    print(
                        f"🔥 OPORTUNIDADE: {c['name']} | R${c['price']}"
                    )

                    add_alert(c)

            time.sleep(60)

        except Exception as e:

            print("ERRO ENGINE:", e)

            time.sleep(15)