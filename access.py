import json
import os

FILE = "vip_users.json"


def load():

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def is_vip(user):

    data = load()

    return user in data


def add_vip(user):

    data = load()

    if user not in data:
        data.append(user)

    save(data)