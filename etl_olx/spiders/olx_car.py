import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OlxCarSpider(scrapy.Spider):
    name = "olx_car"
    allowed_domains = ["www.olx.com.br"]
    start_urls = [
        "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rn?ps=20000&pe=40000&q=honda%20civic&rs=2006&re=2010"]

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    def __init__(self, *args, **kwargs):
        super(OlxCarSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(options=self.options)

    def start_requests(self):
        for url in self.start_urls:
            self.driver.get(url)

            # Espera o elemento ser carregado
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'h2.AdCard_title__5bFRP'))
            )

            # Pegando o HTML completo da página
            html = self.driver.page_source

            # Passando o HTML para o Scrapy
            response = scrapy.http.HtmlResponse(
                url=self.driver.current_url, body=html, encoding='utf-8')

            # Chama o método parse para processar a resposta
            yield from self.parse(response)

            # Fecha o driver após o processo
            self.driver.quit()

    def parse(self, response):
        # Aqui o Scrapy vai gerar os dados para o arquivo JSON
        titles = response.css('h2.AdCard_title__5bFRP::text').getall()
        prices = response.css('h3.AdCard_price___yY62::text').getall()
        links = response.css('a.AdCard_link__4c7W6::attr(href)').getall()

        for title, price, link in zip(titles, prices, links):
            yield {
                'title': title,
                'price': price,
                'link': link
            }
