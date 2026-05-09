import requests

URL = "https://api.pokemontcg.io/v2/cards"

def normalize(text):
    return text.lower().replace(" ", "")

def get_cards(query):

    try:

        response = requests.get(URL, timeout=15)
        data = response.json().get("data", [])

        q = normalize(query)

        results = []

        for card in data:

            name = normalize(card.get("name", ""))
            number = normalize(card.get("number", ""))

            # busca flexível
            if q in name or q == number:
                results.append(card)

        return results

    except Exception as e:

        print("API ERROR:", e)

        return []