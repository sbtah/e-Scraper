from scraper.sites.kiddymoon import KiddyMoon
from scraper.sites.castorama import Castorama
import time
from urllib.parse import urljoin
from lxml.html import tostring
import importlib


websites = [
    ("kiddymoon", "KiddyMoon"),
    ("castorama", "Castorama"),
]

for website in websites:
    try:
        module = importlib.import_module(f"scraper.sites.{website[0]}")
        my_class = getattr(module, f"{website[1]}")
        print(my_class)
    except ModuleNotFoundError:
        print(f"Module was not found: {website[0]}")


# products_urls_kiddy = [
#     "https://kiddymoon.pl/pl/newproducts/nowosc.html",
#     "https://kiddymoon.pl/pl/menu/suche-baseny-1140.html",
#     "https://kiddymoon.pl/pl/menu/pilki-do-basenu-1466.html",
#     "https://kiddymoon.pl/pl/menu/place-zabaw-1480.html",
#     "https://kiddymoon.pl/pl/menu/kitchen-helpery-1465.html",
#     "https://kiddymoon.pl/pl/menu/zabawki-1467.html",
#     "https://kiddymoon.pl/pl/menu/pokoj-dzieciecy-1474.html",
# ]
# products_url_casto = "https://www.castorama.pl/produkty/urzadzanie/zarowki-i-swietlowki/zarowki-led.html"  # noqa


# if __name__ == "__main__":
#     start = time.time()
#     with my_class() as scraper:
#         for url in products_urls_kiddy:
#             response = scraper.selenium_get(
#                 url,
#             )
#             element = scraper.parse_response(response=response)
#             scraper.close_cookies_banner(element=element)
#             products = scraper.find_products_for_all_pages_selenium()
#             for prod in products:
#                 prod
#             scraper.do_cleanup()
#     end = time.time()
#     print(end - start)


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
