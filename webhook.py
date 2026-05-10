from flask import Flask, request
from access import add_vip

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    try:

        user_id = data.get("metadata", {}).get("user_id")

        if user_id:
            add_vip(str(user_id))

            print("VIP LIBERADO:", user_id)

    except Exception as e:
        print("ERRO WEBHOOK:", e)

    return "ok"