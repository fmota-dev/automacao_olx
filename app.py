import os
import sys
import time
import subprocess

# Adiciona a pasta src ao path para que o pacote 'etl_olx' seja encontrado
sys.path.insert(0, os.path.abspath("src"))

# Define o módulo de configurações do Scrapy
os.environ['SCRAPY_SETTINGS_MODULE'] = 'etl_olx.settings'

# Caminho completo para o executável scrapy no ambiente virtual
SCRAPY_EXECUTABLE = os.path.join(
    os.path.abspath(".venv"), "Scripts", "scrapy.exe")

contador = 1
while True:
    try:
        print(f"\nExecução {contador} iniciada...")
        # Define o PYTHONPATH para incluir o diretório raiz do projeto e o diretório src
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{os.path.abspath('.')};{os.path.abspath('src')}"
        # Adiciona o ambiente virtual ao PATH
        env["PATH"] += f";{os.path.abspath('.venv/Scripts')}"

        # Executa o comando scrapy crawl usando o caminho completo do executável
        subprocess.run([SCRAPY_EXECUTABLE, "crawl", "olx_car"],
                       check=True, env=env)
    except subprocess.CalledProcessError as e:
        # Captura erros do subprocesso
        print(f"Erro ao executar o Scrapy: {e}")
    except Exception as e:
        # Captura outros erros
        print(f"Erro inesperado: {e}")

    # Aguarda 10 minutos antes da próxima execução
    tempo_espera = 600
    while tempo_espera > 0:
        minutos = tempo_espera // 60
        segundos = tempo_espera % 60
        print(f"Aguardando {minutos:02}:{segundos:02}...", end="\r")
        time.sleep(1)
        tempo_espera -= 1

    print(f"\nExecução {contador} finalizada! Aguardando 10 minutos...\n")
    contador += 1
