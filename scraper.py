import requests
from bs4 import BeautifulSoup
from config import BASE_URL

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


def scrape_cards(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")

    cards = []

    # ⚠️ seletor genérico (vai ajustar conforme site real)
    items = soup.find_all("div", class_="card")

    for item in items:
        try:
            name = item.find("h3").text.strip()
            rarity = item.find("span", class_="rarity").text.strip()
            link = item.find("a")["href"]

            cards.append({
                "name": name,
                "rarity": rarity,
                "link": BASE_URL + link
            })

        except:
            continue

    return cards