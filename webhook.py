from flask import Flask, request
from db import set_vip

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    try:
        if data["type"] == "payment":

            payment = data["data"]["object"]

            if payment["status"] == "approved":

                user_id = int(payment["external_reference"])
                set_vip(user_id)

                print("VIP ativado:", user_id)

    except Exception as e:
        print("Webhook error:", e)

    return "OK", 200


app.run(host="0.0.0.0", port=5000)