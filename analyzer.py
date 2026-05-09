import math

def analyze(prices, current_price):

    if len(prices) < 5:
        return None

    mean = sum(prices) / len(prices)

    std = math.sqrt(
        sum((x - mean) ** 2 for x in prices) / len(prices)
    )

    if std == 0:
        return None

    z_score = (mean - current_price) / std

    return {
        "mean": mean,
        "score": z_score
    }