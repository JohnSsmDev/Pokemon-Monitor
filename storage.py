import json
import os

FILE = "data/cards.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)