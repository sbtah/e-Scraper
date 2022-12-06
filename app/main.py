from scraper.sites.kiddymoon import KiddyMoon
from scraper.sites.castorama import Castorama
from scraper.logic.validation import ValidationCrawler
from scraper.logic.scraping_scraper import ScrapingScraper
from scraper.options.settings import USER_AGENTS
import time
from urllib.parse import urljoin
from lxml.html import tostring
import importlib
from scraper.helpers.randoms import get_random_user_agent
from scraper.helpers.check_time import calculate_time
from scraper.helpers.logger import logger


products_urls_kiddy = [
    # "https://kiddymoon.pl/",
    "https://kiddymoon.pl/pl/ntst.html",
    "https://kiddymoon.pl/pl/menu/suche-baseny-1140.html",
    "https://kiddymoon.pl/pl/menu/pilki-do-basenu-1466.html",
    "https://kiddymoon.pl/pl/menu/place-zabaw-1480.html",
    "https://kiddymoon.pl/pl/menu/kitchen-helpery-1465.html",
    "https://kiddymoon.pl/pl/menu/zabawki-1467.html",
    "https://kiddymoon.pl/pl/menu/pokoj-dzieciecy-1474.html",
]

products_urls_casto = [
    "https://www.castorama.pl/produkty/urzadzanie/zarowki-i-swietlowki/zarowki-led.html",
]  # noqa

# Scraping Task that should be integrated in Tasker.
# Just for testing. Manually provided url list with all Pages with products.
@calculate_time
def find_product_data():
    for url in products_urls_kiddy:
        validation = ValidationCrawler().validate_page_status(url=url)
        if validation:
            with KiddyMoon() as scraper:
                meta_data = scraper.visit_web_page(url=url)
                print(f"USER-AGENT: {scraper.user_agent}")
                products = scraper.find_product_pages_for_all_pages_selenium(
                    extract_with_selenium=True
                )
                for prod in products:
                    print(prod)
                scraper.do_cleanup()
        else:
            pass


def find_category_data():
    for url in products_urls_kiddy:
        validation = ValidationCrawler().validate_page_status(url=url)
        if validation:
            with KiddyMoon() as scraper:
                meta_data = scraper.visit_web_page(url=url)
                element = scraper.parse_driver_response()
                categories = scraper.find_all_category_pages(
                    html_element=element, find_with_selenium=True
                )
                for cat in categories:
                    print(cat)
                scraper.do_cleanup()
        else:
            pass


def validate_page_status():
    with KiddyMoon() as scraper:
        for url in products_urls_kiddy:
            response = scraper.python_get(url=url)
            print(response)
            print(type(response))


def dumb_test():
    with KiddyMoon() as scraper:
        print(scraper.products_discovery_xpath_dict.get(2))


def test_random_agent():
    agent = get_random_user_agent(USER_AGENTS)
    print(agent)


if __name__ == "__main__":
    find_product_data()
