import requests


def search_cards(query):

    url = "https://api.pokemontcg.io/v2/cards"

    params = {
        "q": f'name:"{query}"'
    }

    r = requests.get(url, params=params)

    data = r.json()

    cards = []

    for c in data.get("data", []):

        try:

            market = c.get("cardmarket", {})

            prices = market.get("prices", {})

            price = prices.get("averageSellPrice")

            if not price:
                continue

            cards.append({
                "name": c["name"],
                "number": c.get("number"),
                "rarity": c.get("rarity"),
                "set": c.get("set", {}).get("name"),
                "image": c.get("images", {}).get("small"),
                "price": price,
                "source": "PokemonTCG"
            })

        except:
            continue

    return cards