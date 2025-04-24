import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timedelta

# Adiciona a pasta src ao path
sys.path.insert(0, os.path.abspath("src"))

# Define o módulo de configurações do Scrapy
os.environ["SCRAPY_SETTINGS_MODULE"] = "etl_olx.settings"

# Detecta o sistema operacional
if platform.system() == "Windows":
    SCRAPY_EXECUTABLE = os.path.join(os.path.abspath(".venv"), "Scripts", "scrapy.exe")
else:
    if "VIRTUAL_ENV" in os.environ:
        SCRAPY_EXECUTABLE = os.path.join(os.environ["VIRTUAL_ENV"], "bin", "scrapy")
    else:
        SCRAPY_EXECUTABLE = "/usr/local/bin/scrapy"

while True:
    try:
        print("🚀 Execução da automação iniciada!", flush=True)

        env = os.environ.copy()
        path_sep = ";" if platform.system() == "Windows" else ":"
        env["PYTHONPATH"] = f"{os.path.abspath('.')}{path_sep}{os.path.abspath('src')}"

        if platform.system() == "Windows":
            env["PATH"] += f";{os.path.abspath('.venv/Scripts')}"
        else:
            env["PATH"] += ":/usr/local/bin"

        subprocess.run([SCRAPY_EXECUTABLE, "crawl", "olx_car"], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o Scrapy: {e}", flush=True)
    except Exception as e:
        print(f"⚠️ Erro inesperado: {e}", flush=True)

    # Calcula a hora da próxima execução
    proxima_execucao = datetime.now() + timedelta(seconds=600)  # 10 minutos de espera

    # Aguarda 10 minutos (600 segundos)
    print("⏳ Aguardando 10 minutos para a próxima execução...")
    print(f"\n🕒 Próxima execução será às {proxima_execucao.strftime('%H:%M:%S')}")

    time.sleep(600)
