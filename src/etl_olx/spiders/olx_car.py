import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

from src.etl_olx.utils.email_utils import send_email


class OlxCarSpider(scrapy.Spider):
    name = "olx_car"
    allowed_domains = ["www.olx.com.br"]
    start_urls = [
        "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rn?ps=20000&pe=40000&q=honda%20civic&rs=2006&re=2010",
        "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rn?q=gol+g5+1.6&o=1"
    ]

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0...')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(options=self.options)

        self.seen_file = '/data/seen_ads.json'

        self.seen_ads = self._load_seen_ads()

    def _load_seen_ads(self):
        self.logger.info("Loading seen ads...")
        if os.path.exists(self.seen_file):
            with open(self.seen_file, 'r') as f:
                seen_ads = json.load(f)
                self.logger.info(f"Loaded {len(seen_ads)} seen ads.")
                return seen_ads
        return {}

    def _save_seen_ads(self):
        os.makedirs(os.path.dirname(self.seen_file), exist_ok=True)
        with open(self.seen_file, 'w') as f:
            json.dump(self.seen_ads, f)
        self.logger.info(f"Saved {len(self.seen_ads)} seen ads.")

    def start_requests(self):
        for url in self.start_urls:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'h2.AdCard_title__5bFRP'))
                )

                html = self.driver.page_source
                response = scrapy.http.HtmlResponse(
                    url=self.driver.current_url, body=html, encoding='utf-8')
                yield from self.parse(response)
            except Exception as e:
                self.logger.error(f"Error processing {url}: {e}")
            finally:
                self._save_seen_ads()

    def parse(self, response):
        titles = response.css('h2.AdCard_title__5bFRP::text').getall()
        prices = response.css('h3.AdCard_price___yY62::text').getall()
        links = response.css('a.AdCard_link__4c7W6::attr(href)').getall()

        for title, price, link in zip(titles, prices, links):
            unique_id = f"{title} - {price} - {link}"
            if unique_id not in self.seen_ads:
                self.seen_ads[unique_id] = True
                send_email(title, price, link)
                yield {
                    'title': title,
                    'price': price,
                    'link': link
                }

    def closed(self, reason):
        # Garantir que o driver será fechado ao final
        self.driver.quit()
