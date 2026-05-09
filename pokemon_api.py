import requests

URL = "https://api.pokemontcg.io/v2/cards"

def get_cards(name):

    try:

        params = {
            "q": f'name:"{name}"'
        }

        response = requests.get(
            URL,
            params=params,
            timeout=15
        )

        data = response.json()

        return data.get("data", [])

    except Exception as e:

        print("ERRO API:", e)

        return []