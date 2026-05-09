import os
import requests

MP_TOKEN = os.getenv("MP_TOKEN")

def create_payment(user_id):

    url = "https://api.mercadopago.com/v1/payments"

    headers = {
        "Authorization": f"Bearer {MP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "transaction_amount": 19.9,
        "description": "VIP Pokemon Bot",
        "payment_method_id": "pix",
        "external_reference": str(user_id),
        "payer": {
            "email": f"user{user_id}@bot.com"
        }
    }

    r = requests.post(url, json=payload, headers=headers)

    return r.json()