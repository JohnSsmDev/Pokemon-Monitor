import statistics

def calcular_score(preco, media, historico):

    if media == 0:
        return 0

    desconto = ((media - preco) / media) * 100

    if len(historico) > 3:
        media_hist = statistics.mean(historico[-5:])
    else:
        media_hist = media

    queda = ((media_hist - preco) / media_hist) * 100

    score = (desconto * 0.6) + (queda * 0.4)

    return score