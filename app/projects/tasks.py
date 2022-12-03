from scraper.sites.kiddymoon import KiddyMoon
from scraper.sites.castorama import Castorama
import time
from urllib.parse import urljoin
from lxml.html import tostring
import importlib
from scraper.helpers.check_time import calculate_time
from celery import shared_task
from scraper.helpers.logger import logger

# websites = [
#     ("kiddymoon", "KiddyMoon"),
#     ("castorama", "Castorama"),
# ]

# for website in websites:
#     try:
#         module = importlib.import_module(f"scraper.sites.{website[0]}")
#         my_class = getattr(module, f"{website[1]}")
#         print(my_class)
#     except ModuleNotFoundError:
#         print(f"Module was not found: {website[0]}")


products_urls_kiddy = [
    "https://kiddymoon.pl/",
    # "https://kiddymoon.pl/pl/newproducts/nowosc.html",
    # "https://kiddymoon.pl/pl/menu/suche-baseny-1140.html",
    # "https://kiddymoon.pl/pl/menu/pilki-do-basenu-1466.html",
    # "https://kiddymoon.pl/pl/menu/place-zabaw-1480.html",
    # "https://kiddymoon.pl/pl/menu/kitchen-helpery-1465.html",
    # "https://kiddymoon.pl/pl/menu/zabawki-1467.html",
    # "https://kiddymoon.pl/pl/menu/pokoj-dzieciecy-1474.html",
]
# products_url_casto = "https://www.castorama.pl/produkty/urzadzanie/zarowki-i-swietlowki/zarowki-led.html"  # noqa


@shared_task
# @calculate_time
def scraping_task_products():
    with KiddyMoon() as scraper:
        for url in products_urls_kiddy:
            response = scraper.selenium_get(
                url,
            )
            element = scraper.parse_response(response=response)
            scraper.close_cookies_banner(element=element)
            products = scraper.find_products_for_all_pages_selenium()
            for prod in products:
                prod
            scraper.do_cleanup()


@shared_task
# @calculate_time
def scraping_task_scroll():
    with KiddyMoon() as scraper:
        try:
            for url in products_urls_kiddy:
                response = scraper.selenium_get(
                    url,
                )
                element = scraper.parse_response(response=response)
                scraper.close_cookies_banner(element=element)
                time.sleep(5)
                element = scraper.find_selenium_element(
                    xpath_to_search='.//button[@name="mailing_action"]',
                )
                scraper.scroll_to_element(selenium_element=element)
                time.sleep(5)
                scraper.do_cleanup()
            return True
        except Exception as e:
            # logger.error("Some other exception")
            return None


# if __name__ == "__main__":
#     scraping_task_scroll.delay()
