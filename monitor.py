import requests
import time
import sqlite3
from datetime import datetime

# conexão banco
conexao = sqlite3.connect("pokemon.db")

cursor = conexao.cursor()

cartas_monitoradas = [
    "Rayquaza",
    "Umbreon",
    "Charizard",
    "Pikachu"
]

preco_alvo = 20

while True:

    print("\n===== MONITOR POKÉMON =====\n")

    ranking = []

    for nome_carta in cartas_monitoradas:

        try:

            url = "https://api.pokemontcg.io/v2/cards"

            parametros = {
                "q": f'name:"{nome_carta}"'
            }

            response = requests.get(url, params=parametros)

            dados = response.json()

            if "data" not in dados:
                continue

            cartas = dados["data"]

            for carta in cartas:

                if "cardmarket" not in carta:
                    continue

                preco = carta["cardmarket"]["prices"]["averageSellPrice"]

                nome = carta["name"]

                numero = carta.get("number", "Desconhecido")

                colecao = carta.get("set", {}).get("name", "Desconhecida")

                raridade = carta.get("rarity", "Desconhecida")

                imagem = carta.get("images", {}).get("small", "")

                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # salva banco
                cursor.execute("""
                INSERT INTO cartas (
                    nome,
                    numero,
                    colecao,
                    raridade,
                    preco,
                    imagem,
                    data_hora
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    nome,
                    numero,
                    colecao,
                    raridade,
                    preco,
                    imagem,
                    data_hora
                ))

                conexao.commit()

                ranking.append({
                    "nome": nome,
                    "numero": numero,
                    "colecao": colecao,
                    "raridade": raridade,
                    "preco": preco,
                    "imagem": imagem
                })

        except Exception as erro:
            print("ERRO:", erro)

    # ordena pelo menor preço
    ranking = sorted(ranking, key=lambda x: x["preco"])

    print("\n===== TOP OPORTUNIDADES =====\n")

    for i, carta in enumerate(ranking[:10], start=1):

        print(f"{i}. {carta['nome']}")
        print(f"Número: {carta['numero']}")
        print(f"Coleção: {carta['colecao']}")
        print(f"Raridade: {carta['raridade']}")
        print(f"Preço: ${carta['preco']}")

        if carta["preco"] < preco_alvo:
            print("🔥 OPORTUNIDADE ENCONTRADA!")

        print("-" * 40)

    print("\nNova verificação em 60 segundos...\n")

    time.sleep(60)