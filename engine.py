import time

def start():
    print("📡 ENGINE INICIADO")

    while True:
        try:
            # SIMULAÇÃO DO SCRAPER (substitui depois)
            print("🔍 Monitorando preços...")

            # aqui entra seu scraping real depois
            time.sleep(10)

        except Exception as e:
            print("❌ ERRO ENGINE:", e)
            time.sleep(5)