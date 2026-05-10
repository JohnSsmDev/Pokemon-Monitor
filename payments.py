import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("PUSHINPAY_TOKEN")


def create_pix_payment(user_id):

    url = "https://api.pushinpay.com.br/api/pix/cashIn"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "value": 19.90,
        "webhook_url": "https://SEU-APP.up.railway.app/webhook"
    }

    r = requests.post(
        url,
        json=payload,
        headers=headers
    )

    data = r.json()

    return {
        "pix_code": data.get("qr_code"),
        "payment_id": data.get("id")
    }