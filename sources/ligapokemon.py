import requests
from bs4 import BeautifulSoup


def search_liga(query):

    url = f"https://www.ligapokemon.com.br/?view=cards/search&card={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    cards = []

    produtos = soup.select(".card-item")

    for p in produtos:

        try:

            nome = p.select_one(".card-name").text.strip()

            preco = (
                p.select_one(".price")
                .text
                .replace("R$", "")
                .replace(",", ".")
                .strip()
            )

            link = p.select_one("a")["href"]

            cards.append({
                "name": nome,
                "price": float(preco),
                "source": "LigaPokemon",
                "link": link
            })

        except:
            continue

    return cards