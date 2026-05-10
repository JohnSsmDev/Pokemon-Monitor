import time
import requests
from bs4 import BeautifulSoup
from storage import load_data, save_data
from alerts import send_alert

URL = "https://www.ligapokemon.com.br/cards"  # ajustar depois

RARITY_FILTER = ["UR", "AR", "SR", "Full Art"]

def fetch_page():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=20)
    r.raise_for_status()
    return r.text


def parse_cards(html):
    soup = BeautifulSoup(html, "html.parser")

    cards = []

    items = soup.find_all("div", class_="card")

    for item in items:
        try:
            name = item.find("h3").text.strip()
            rarity = item.find("span", class_="rarity").text.strip()
            link = item.find("a")["href"]

            cards.append({
                "name": name,
                "rarity": rarity,
                "link": link
            })
        except:
            continue

    return cards


def filter_cards(cards):
    return [
        c for c in cards
        if any(r in c["rarity"] for r in RARITY_FILTER)
    ]


def detect_new(old, new):
    old_names = {c["name"] for c in old}
    return [c for c in new if c["name"] not in old_names]


def start():
    print("📡 ENGINE INICIADO")

    while True:
        try:
            old_data = load_data()

            html = fetch_page()
            cards = parse_cards(html)
            filtered = filter_cards(cards)

            new_cards = detect_new(old_data, filtered)

            if new_cards:
                for card in new_cards:
                    send_alert(
                        f"🔥 OPORTUNIDADE DETECTADA\n\n"
                        f"🃏 {card['name']}\n"
                        f"⭐ {card['rarity']}\n"
                        f"🔗 {card['link']}"
                    )

            save_data(filtered)

            print(f"✔ ciclo OK | novos: {len(new_cards)}")

        except Exception as e:
            print("ERRO ENGINE:", e)

        time.sleep(300)  # 5 min