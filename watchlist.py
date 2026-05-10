import json
import os

FILE = "watchlist.json"


def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_watch(user, query):

    data = load()

    if user not in data:
        data[user] = []

    if query not in data[user]:
        data[user].append(query)

    save(data)


def get_watchs(user):

    data = load()

    return data.get(user, [])