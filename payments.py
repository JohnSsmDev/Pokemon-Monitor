import os
import mercadopago

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

def create_payment(user_id):

    preference_data = {
        "items": [
            {
                "title": "VIP Pokemon Bot",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 9.90
            }
        ],
        "external_reference": str(user_id)
    }

    preference = sdk.preference().create(preference_data)

    return preference["response"]