from bot import send_alert
import time

print("🚀 INICIANDO TESTE RAILWAY")

# TESTE DIRETO TELEGRAM
send_alert("🚀 TESTE DIRETO DO RAILWAY")

print("✅ ALERTA TESTADO")

# Loop simples pra manter worker vivo
while True:

    print("MONITORANDO MERCADO...")

    time.sleep(30)