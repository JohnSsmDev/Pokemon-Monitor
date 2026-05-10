def detect_changes(old_data, new_data):
    old_names = {c["name"] for c in old_data}

    new_cards = []

    for card in new_data:
        if card["name"] not in old_names:
            new_cards.append(card)

    return new_cards