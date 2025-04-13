import os
import time

contador = 1

while True:
    print(f"Execução {contador} iniciada...")

    os.system("scrapy crawl olx_car")

    tempo_espera = 600
    while tempo_espera > 0:
        minutos = tempo_espera // 60
        segundos = tempo_espera % 60
        print(
            f"Aguardando {minutos:02}:{segundos:02} para a próxima execução...", end="\r")
        time.sleep(1)
        tempo_espera -= 1

    print(
        f"\nExecução {contador} finalizada! Aguardando 10 minutos para a próxima execução...\n")

    contador += 1
