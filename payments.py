from flask import Flask, request
from access import activate_vip

app = Flask(__name__)

def start():
    print("💰 PAYMENTS ON")
    app.run(host="0.0.0.0", port=5000)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data.get("status") == "approved":
        user_id = data.get("external_reference")
        activate_vip(user_id)

    return "ok"