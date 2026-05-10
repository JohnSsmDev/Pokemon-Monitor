import time
from marketplace import search_cards
from access import add_alert

WATCHLIST = ["charizard", "umbreon", "pikachu", "rayquaza"]

def score(card):
    s = 0

    if card["price"] < card["avg"] * 0.7:
        s += 50

    if card["name"].lower() in WATCHLIST:
        s += 30

    if card["rarity"] in ["Ultra Rare", "Secret Rare"]:
        s += 20

    return s

def start():
    print("📡 ENGINE RODANDO")

    while True:
        for q in WATCHLIST:
            cards = search_cards(q)

            for c in cards:
                s = score(c)

                if s >= 60:
                    c["score"] = s
                    add_alert(c)

        time.sleep(20)