import os
import sys
import time
import subprocess
import platform

# Adiciona a pasta src ao path
sys.path.insert(0, os.path.abspath("src"))

# Define o módulo de configurações do Scrapy
os.environ['SCRAPY_SETTINGS_MODULE'] = 'etl_olx.settings'

# Detecta o sistema operacional
if platform.system() == "Windows":
    SCRAPY_EXECUTABLE = os.path.join(
        os.path.abspath(".venv"), "Scripts", "scrapy.exe")
else:
    # No Docker, Scrapy será instalado globalmente, então vamos utilizar o caminho correto
    if "VIRTUAL_ENV" in os.environ:
        SCRAPY_EXECUTABLE = os.path.join(
            os.environ["VIRTUAL_ENV"], "bin", "scrapy")
    else:
        # Caso não esteja no ambiente virtual, assume o caminho global no Docker
        # Caminho global do Scrapy no Docker
        SCRAPY_EXECUTABLE = "/usr/local/bin/scrapy"

contador = 1
while True:
    try:
        print(f"\nExecução {contador} iniciada...", flush=True)

        env = os.environ.copy()
        path_sep = ";" if platform.system() == "Windows" else ":"
        env["PYTHONPATH"] = f"{os.path.abspath('.')}{path_sep}{os.path.abspath('src')}"

        # Adiciona o bin do venv ao PATH no Windows
        if platform.system() == "Windows":
            env["PATH"] += f";{os.path.abspath('.venv/Scripts')}"
        else:
            # No Docker, o caminho do bin do Scrapy está global, então ajusta o PATH
            env["PATH"] += f":/usr/local/bin"  # Scrapy global no Docker

        # Executa o Scrapy com as variáveis de ambiente
        subprocess.run([SCRAPY_EXECUTABLE, "crawl", "olx_car"],
                       check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o Scrapy: {e}", flush=True)
    except Exception as e:
        print(f"Erro inesperado: {e}", flush=True)

    # Aguarda 10 minutos antes da próxima execução
    tempo_espera = 600
    while tempo_espera > 0:
        minutos = tempo_espera // 60
        segundos = tempo_espera % 60
        print(f"Aguardando {minutos:02}:{segundos:02}...",
              end="\r", flush=True)
        time.sleep(1)
        tempo_espera -= 1

    print(
        f"\nExecução {contador} finalizada! Aguardando 10 minutos...\n")
    contador += 1
