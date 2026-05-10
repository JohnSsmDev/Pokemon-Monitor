import requests


def search_cards(query):

    url = "https://api.pokemontcg.io/v2/cards"

    # busca por número
    if "/" in query:

        base_number = query.split("/")[0]

        search_query = (
            f'number:"{query}" OR number:"{base_number}"'
        )

    # busca por nome
    else:

        search_query = f'name:*{query}*'

    params = {
        "q": search_query,
        "pageSize": 10
    }

    r = requests.get(url, params=params)

    data = r.json()

    cards = []

    for c in data.get("data", []):

        try:

            market = c.get("cardmarket", {})
            prices = market.get("prices", {})

            price = (
                prices.get("averageSellPrice")
                or prices.get("trendPrice")
                or 0
            )
            match_score = 0

            if c.get("number") == query:
                match_score += 100

            rarity = str(c.get("rarity", "")).lower()

            rare_words = [
                "secret",
                "ultra",
                "illustration",
                "hyper",
                "full"
            ]

            for w in rare_words:
                if w in rarity:
                    match_score += 30

                cards.append({
                "name": c.get("name"),
                "number": c.get("number"),
                "rarity": c.get("rarity"),
                "set": c.get("set", {}).get("name"),
                "image": c.get("images", {}).get("large"),
                "price": round(float(price), 2),
                "source": "PokemonTCG",
                "match_score": match_score
})

        except:
            continue
            cards = sorted(
    cards,
    key=lambda x: x["match_score"],
    reverse=True
)
    return cards