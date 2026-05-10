import requests

API_URL = "https://api.pokemontcg.io/v2/cards"

def get_card_data(card_name):

    url = f"{API_URL}?q=name:{card_name}"

    r = requests.get(url)

    data = r.json()

    cards = data.get("data", [])

    if not cards:
        return None

    card = cards[0]

    market_price = None

    tcgplayer = card.get("tcgplayer")

    if tcgplayer:

        prices = tcgplayer.get("prices", {})

        if "holofoil" in prices:
            market_price = prices["holofoil"].get("market")

        if not market_price:

            for p in prices.values():

                market_price = p.get("market")

                if market_price:
                    break

    return {
        "name": card["name"],
        "set": card["set"]["name"],
        "number": card["number"],
        "image": card["images"]["small"],
        "price": market_price
    }