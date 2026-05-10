import requests
import time
import sqlite3
from datetime import datetime

def start_monitor():
    conexao = sqlite3.connect("pokemon.db", check_same_thread=False)
    cursor = conexao.cursor()

    cartas = ["Rayquaza", "Umbreon", "Charizard", "Pikachu"]
    preco_alvo = 20

    while True:
        print("\n===== MONITOR POKÉMON =====\n")

        ranking = []

        for nome in cartas:
            try:
                url = "https://api.pokemontcg.io/v2/cards"
                r = requests.get(url, params={"q": f'name:"{nome}"'})
                data = r.json()

                if "data" not in data:
                    continue

                for c in data["data"]:
                    if "cardmarket" not in c:
                        continue

                    preco = c["cardmarket"]["prices"]["averageSellPrice"]

                    ranking.append({
                        "nome": c["name"],
                        "preco": preco
                    })

            except Exception as e:
                print("ERRO:", e)

        ranking.sort(key=lambda x: x["preco"])

        for i, c in enumerate(ranking[:10], 1):
            print(f"{i}. {c['nome']} - ${c['preco']}")

        print("⏳ aguardando 60s...\n")
        time.sleep(60)