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
    "https://misioohandmade.pl/sklep/",
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


def find_category_data_misio():
    for url in urls_misioo:
        validatation = ValidationCrawler().validate_page_status(url=url)
        if validatation:
            with MisioHandMade() as scraper:
                meta_data = scraper.visit_web_page(url=url)
                print(meta_data)
                element = scraper.parse_driver_response
                categories = scraper.find_all_category_pages(html_element=element)
                for cat in categories:
                    print(cat)
                scraper.do_cleanup()
        else:
            pass


def validate_page_status():
    with KiddyMoon() as scraper:
        for url in urls_kiddy:
            response = scraper.python_get(url=url)
            print(response)
            print(type(response))


def dumb_test():
    with KiddyMoon() as scraper:
        scraper.visit_web_page(url=urls_kiddy[0])
        element = scraper.parse_driver_response()

        categories = scraper.find_all_category_pages(
            html_element=element,
            category_level=1,
            parser_used=scraper.categories_parsers_dict_by_level[1],
            extract_with_selenium=True,
        )
        # categories = scraper.extract_urls_with_names(
        #     html_element=element,
        #     xpath_to_search=scraper.categories_discovery_xpath_dict[1][
        #         "category_element_xpath"
        #     ],
        #     name_attr_xpath=scraper.categories_discovery_xpath_dict[1][
        #         "category_name_xpath"
        #     ],
        #     parser_used=scraper.parse_category_level_1_elements,
        #     extract_with_selenium=False,
        # )
        # categories = scraper.find_selenium_elements(
        #     xpath_to_search=scraper.categories_discovery_xpath_dict[1][
        #         "category_url_xpath"
        #     ],
        # )
        for cat in categories:
            print(cat)


def test_random_agent():
    agent = get_random_user_agent(USER_AGENTS)
    print(agent)


if __name__ == "__main__":
    find_product_data()
