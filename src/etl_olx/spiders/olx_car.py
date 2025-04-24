import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.etl_olx.utils.email_utils import send_ad_email
from src.etl_olx.utils.db import ad_exists, save_ad, create_table_if_needed


class OlxCarSpider(scrapy.Spider):
    name = "olx_car"
    allowed_domains = ["www.olx.com.br"]
    start_urls = [
        "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rn?ps=20000&pe=40000&q=honda%20civic&rs=2006&re=2010",
        "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rn?ps=20000&pe=30000&q=gol%201.6&rs=2009&re=2012",
    ]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0...")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(options=self.options)
        create_table_if_needed()

    def start_requests(self):
        new_ads_count = 0  # Variável para contar os anúncios novos

        for url in self.start_urls:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "section.olx-adcard")
                    )
                )
                html = self.driver.page_source
                response = scrapy.http.HtmlResponse(
                    url=self.driver.current_url, body=html, encoding="utf-8"
                )
                new_ads_count += yield from self.parse(
                    response
                )  # A contagem é atualizada a cada parse
            except Exception as e:
                print(f"❌ [ERRO] Erro ao processar {url}: {e}")

        # Verifica no final de todos os URLs processados
        if new_ads_count == 0:
            print("🔴 Nenhum anúncio novo encontrado.")
        else:
            print(f"✅ {new_ads_count} novos anúncios encontrados e salvos.")

    def parse(self, response):
        titles = response.css("h2.olx-adcard__title::text").getall()
        prices = response.css("h3.olx-adcard__price::text").getall()
        links = response.css("a.olx-adcard__link::attr(href)").getall()

        new_ads_count = 0  # Contador de novos anúncios para esta página

        for title, price, link in zip(titles, prices, links):
            try:
                if not ad_exists(link):
                    save_ad(title, price, link)
                    send_ad_email(title, price, link)
                    print(f"✨ Novo anúncio salvo: {title} - {price}")
                    new_ads_count += 1
                    yield {"title": title, "price": price, "link": link}
            except Exception as e:
                print(f"❌ [ERRO DB] {title} - {link}: {e}")

        return new_ads_count  # Retorna a contagem dos anúncios novos encontrados

    def closed(self, reason):
        self.driver.quit()
        print("🔵 Driver do Selenium fechado corretamente.")
