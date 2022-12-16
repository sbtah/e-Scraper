from scraper.sites.kiddymoon import KiddyMoon
from scraper.sites.misiohandmade import MisioHandMade
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
from selenium.webdriver.common.by import By

urls_kiddy = [
    # "https://kiddymoon.pl/",
    "https://kiddymoon.pl/pl/ntst.html",
    "https://kiddymoon.pl/pl/newproducts/nowosc.html",
    "https://kiddymoon.pl/pl/menu/suche-baseny-1140.html",
    "https://kiddymoon.pl/pl/menu/pilki-do-basenu-1466.html",
    "https://kiddymoon.pl/pl/menu/place-zabaw-1480.html",
    "https://kiddymoon.pl/pl/menu/kitchen-helpery-1465.html",
    "https://kiddymoon.pl/pl/menu/zabawki-1467.html",
    "https://kiddymoon.pl/pl/menu/pokoj-dzieciecy-1474.html",
]


urls_casto = [
    "https://www.castorama.pl/produkty/urzadzanie/zarowki-i-swietlowki/zarowki-led.html",
]  # noqa


urls_misioo = [
    # "https://misioohandmade.pl/",
    "https://misioohandmade.pl/sklep/",
    # "https://misioohandmade.pl/suche-baseny-z-pileczkami/",
]


# Scraping Task that should be integrated in Tasker.
# Just for testing. Manually provided url list with all Pages with products.
@calculate_time
def find_product_data():
    for url in urls_kiddy:
        validation = ValidationCrawler().validate_page_status(url=url)
        if validation:
            with KiddyMoon() as scraper:
                meta_data = scraper.visit_web_page(url=url)
                products = scraper.find_product_pages_for_all_pages_selenium(
                    parser_used=scraper.parse_product_level_1_elements,
                    extract_with_selenium=True,
                )
                for prod in products:
                    print(prod)
                scraper.do_cleanup()
        else:
            pass


@calculate_time
def find_category_data():
    for url in urls_kiddy:
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


##############
@calculate_time
def find_product_data_misioo():
    for url in urls_misioo:
        validatation = ValidationCrawler().validate_page_status(url=url)
        if validatation:
            with MisioHandMade() as scraper:
                meta_data = scraper.visit_web_page(url=url)
                print(meta_data)
                products = scraper.find_product_pages_for_all_pages_selenium(
                    parser_used=scraper.parse_product_level_1_elements,
                    extract_with_selenium=False,
                )
                for prod in products:
                    print(prod)
                scraper.do_cleanup()
        else:
            pass


@calculate_time
def find_category_data_misio():
    for url in urls_misioo:
        validatation = ValidationCrawler().validate_page_status(url=url)
        if validatation:
            with MisioHandMade() as scraper:
                meta_data = scraper.visit_web_page(url=url)
                print(meta_data)
                element = scraper.parse_driver_response()
                categories = scraper.find_all_category_pages(
                    html_element=element,
                    parser_used=scraper.parse_category_level_1_elements,
                )
                for cat in categories:
                    print(cat)
                scraper.do_cleanup()
        else:
            pass


if __name__ == "__main__":
    find_category_data_misio()
