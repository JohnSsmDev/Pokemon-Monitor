def calculate_score(price, average):

    if average == 0:
        return 0

    # quanto abaixo da média
    diff = (average - price) / average

    # score simples
    score = diff * 10

    return round(score, 2)