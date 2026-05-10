import requests

def search_cards(query):
    url = "https://api.pokemontcg.io/v2/cards"
    r = requests.get(url, params={"q": query})
    data = r.json()

    results = []

    for c in data.get("data", []):
        try:
            price = c["cardmarket"]["prices"]["averageSellPrice"]

            results.append({
                "name": c["name"],
                "number": c.get("number"),
                "rarity": c.get("rarity", "Unknown"),
                "price": price,
                "avg": price * 1.25
            })
        except:
            continue

    return results