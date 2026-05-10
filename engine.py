import time

from sources.ligapokemon import search_liga
from access import add_alert

SEARCHES = [
    "charizard",
    "umbreon",
    "pikachu",
]

sent = set()


def calculate_score(card):

    score = 0

    name = card["name"].lower()
    price = card["price"]

    if price < 100:
        score += 30

    if price < 50:
        score += 30

    hot = [
        "charizard",
        "umbreon",
        "pikachu",
    ]

    for h in hot:
        if h in name:
            score += 25

    return score


def start():

    print("📡 ENGINE ONLINE")

    while True:

        try:

            for q in SEARCHES:

                print(f"\n🔍 BUSCANDO: {q}")

                cards = search_liga(q)

                print(f"📦 CARDS ENCONTRADOS: {len(cards)}")

                for c in cards:

                    print("CARD:", c)

                    score = calculate_score(c)

                    print("SCORE:", score)

                    # DEBUG ↓↓↓
                    if score >= 10:

                        key = f"{c['name']}-{c['price']}"

                        if key in sent:
                            continue

                        sent.add(key)

                        c["score"] = score

                        print(
                            f"🔥 ALERTA GERADO: {c['name']}"
                        )

                        add_alert(c)

            time.sleep(60)

        except Exception as e:

            print("❌ ERRO ENGINE:", e)

            time.sleep(10)