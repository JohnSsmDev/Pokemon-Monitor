import time
import asyncio

from sources.pokemon_api import search_cards
from watchlist import load
from notifier import send_alert


def calculate_score(card):

    score = 0

    rarity = str(card.get("rarity", "")).lower()

    rare_words = [
        "secret",
        "ultra",
        "illustration",
        "hyper",
        "full"
    ]

    for w in rare_words:

        if w in rarity:
            score += 30

    if card.get("price", 9999) < 50:
        score += 20

    return score


def run_engine():

    print("📡 ENGINE INICIADO")

    already_sent = set()

    while True:

        try:

            data = load()

            for user_id, queries in data.items():

                for q in queries:

                    cards = search_cards(q)

                    for c in cards[:3]:

                        score = calculate_score(c)

                        if score < 30:
                            continue

                        unique_id = (
                            f"{user_id}-{c['name']}-{c['price']}"
                        )

                        if unique_id in already_sent:
                            continue

                        already_sent.add(unique_id)

                        msg = (
                            f"🔥 OPORTUNIDADE DETECTADA\n\n"
                            f"🃏 {c['name']}\n"
                            f"🏆 {c['rarity']}\n"
                            f"📦 {c['set']}\n"
                            f"💰 ${c['price']}\n"
                            f"⭐ Score: {score}"
                        )

                        asyncio.run(
                            send_alert(
                                user_id,
                                msg,
                                c["image"]
                            )
                        )

                        print("ALERTA ENVIADO")

            time.sleep(300)

        except Exception as e:

            print("ERRO ENGINE:", e)

            time.sleep(60)