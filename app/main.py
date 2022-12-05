from scraper.sites.kiddymoon import KiddyMoon
from scraper.sites.castorama import Castorama
from scraper.logic.scraping_scraper import ScrapingScraper
import time
from urllib.parse import urljoin
from lxml.html import tostring
import importlib
from scraper.helpers.check_time import calculate_time
from scraper.helpers.logger import logger


products_urls_kiddy = [
    # "https://kiddymoon.pl/",
    "https://kiddymoon.pl/pl/newproducts/nowosc.html",
    "https://kiddymoon.pl/pl/menu/suche-baseny-1140.html",
    # "https://kiddymoon.pl/pl/menu/pilki-do-basenu-1466.html",
    # "https://kiddymoon.pl/pl/menu/place-zabaw-1480.html",
    # "https://kiddymoon.pl/pl/menu/kitchen-helpery-1465.html",
    # "https://kiddymoon.pl/pl/menu/zabawki-1467.html",
    # "https://kiddymoon.pl/pl/menu/pokoj-dzieciecy-1474.html",
]

products_urls_casto = [
    "https://www.castorama.pl/produkty/urzadzanie/zarowki-i-swietlowki/zarowki-led.html",
]  # noqa


def find_product_data():
    with KiddyMoon() as scraper:
        for url in products_urls_kiddy:
            response = scraper.selenium_get(
                url,
            )
            element = scraper.parse_response(response=response)
            scraper.close_cookies_banner(element=element)
            products = scraper.find_product_pages_for_all_pages_selenium()
            for prod in products:
                prod
            scraper.do_cleanup()


@calculate_time
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
        except Exception as e:
            # logger.error("Some other exception")
            return None

    return True


if __name__ == "__main__":
    find_product_data()

### GET ELEMENT WITH SELENIUM
# response = scraper.selenium_get(scraper.main_url)
# element = scraper.parse_response(response=response)
# categories_to_track = scraper.extract_urls_with_names_selenium(
#     xpath_to_search=scraper.main_categories_xpath,
#     url_name_attr="title",
# )
# for cat in categories_to_track:
#     print(cat)

### GET ELEMENT WITH PYTHON
# response = scraper.selenium_get(scraper.main_url)
# element = scraper.parse_response(response=response)
# categories_to_track = scraper.find_all_elements(
#     html_element=element,
#     xpath_to_search=scraper.main_categories_xpath,
#     # name_xpath="./@title",
# )
# print(categories_to_track)
# for cat in categories_to_track:
#     print(cat.xpath("./@href")[0])
# response_python = scraper.python_get(scraper.main_url)
# with open(f"response-python.txt", "w") as f:
#     f.write(response_python)
# python_el = scraper.parse_response(response_python)
# with open(f"element-python.txt", "w") as f:
#     elem = tostring(python_el)
#     f.write(str(elem))

# response_selenium = scraper.selenium_get(scraper.main_url)
# with open(f"response-selenium.txt", "w") as f:
#     f.write(response_selenium)
# selenium_el = scraper.parse_response(response_selenium)
# with open(f"element-selenium.txt", "w") as f:
#     elem = tostring(selenium_el)
#     f.write(str(elem))
