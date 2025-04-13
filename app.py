import os
import sys
import time
from scrapy.cmdline import execute

# Adiciona a pasta src ao path para que o pacote 'etl_olx' seja encontrado
sys.path.insert(0, os.path.abspath("src"))

# Define o módulo de configurações do Scrapy
os.environ['SCRAPY_SETTINGS_MODULE'] = 'etl_olx.settings'

contador = 1
while True:
    print(f"\nExecução {contador} iniciada...")
    execute(["scrapy", "crawl", "olx_car"])

    tempo_espera = 600
    while tempo_espera > 0:
        minutos = tempo_espera // 60
        segundos = tempo_espera % 60
        print(f"Aguardando {minutos:02}:{segundos:02}...", end="\r")
        time.sleep(1)
        tempo_espera -= 1

    print(f"\nExecução {contador} finalizada! Aguardando 10 minutos...\n")
    contador += 1
