def send_alert(message):
    """
    Camada segura de alerta.
    NÃO usa Telegram direto aqui para evitar conflito.
    """

    print("📢 ALERTA:", message)

    # depois vamos plugar isso no bot via fila segura