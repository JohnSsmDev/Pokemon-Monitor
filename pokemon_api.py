import requests
import re

URL = "https://api.pokemontcg.io/v2/cards"

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

def get_cards(query):

    try:

        response = requests.get(URL, timeout=15)
        data = response.json().get("data", [])

        q = normalize(query)

        results = []

        for card in data:

            name = normalize(card.get("name", ""))
            number = normalize(card.get("number", ""))
            set_number = normalize(card.get("number", ""))

            card_id = normalize(card.get("id", ""))

            # MATCH INTELIGENTE:
            if (
                q in name or
                q == number or
                q == set_number or
                q in card_id
            ):
                results.append(card)

        return results

    except Exception as e:

        print("API ERROR:", e)

        return []