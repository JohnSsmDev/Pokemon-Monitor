import os
from flask import Flask, request
from Main.db import set_vip

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    status = data.get("status")

    user_id = data.get("external_reference")

    if status == "approved" and user_id:

        set_vip(int(user_id))

        print(f"VIP LIBERADO: {user_id}")

    return "ok"


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )