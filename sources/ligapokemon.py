import requests


def search_liga(query):

    url = f"https://www.ligapokemon.com.br/?view=cards/search&card={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    print("\n===== HTML RECEBIDO =====\n")
    print(r.text[:5000])

    return []