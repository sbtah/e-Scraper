from scraper.logic.scraping_scraper import ScrapingScraper
from urllib.parse import urljoin


class Castorama(ScrapingScraper):
    """
    Specialized scraper for Castorama store.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        return "https://www.castorama.pl/"

    @property
    def main_categories_url(self):
        return "https://www.castorama.pl/"

    @property
    def blog_page_url(self):
        return None

    @property
    def cookies_close_xpath(self):
        return './/button[@name="Zaakceptuj wszystkie"]'

    @property
    def categories_discovery_xpath_dict(self):
        return {
            1: {
                "category_element_xpath": './/ul[contains(@class, "level1")]/li[./a]/a',
            },
            2: {},
            3: {},
        }

    @property
    def all_products_xpath(self):
        return './/div[contains(@class, "product-tail__image")]/a[contains(@class, "link-base") and @title]'

    @property
    def products_names_attribute_xpath(self):
        """Xpath that product's name from url. Example: text(), or @title"""
        return "./@title"

    @property
    def current_product_page_xpath(self):
        return './/ul[contains(@class, "navigation-base")]//li[contains(@class, "base__item") and .//a[contains(@class, "--active")]]'

    @property
    def last_product_page_xpath(self):
        """Explicit Xpath that returns value of last product page"""
        # Currently you can't find last page xpath.
        return ""

    @property
    def next_product_page_button_xpath(self):
        """Xpath that returns selenium webelement to be clicked."""
        return './/ul[contains(@class, "navigation-base")]//li[contains(@class, "base__next") and .//a[contains(@class, "link--active")]]'

    def parse_category_level_1_elements(
        self,
        HtmlElement,
        SeleniumWebElement,
    ):
        category_url_raw = HtmlElement.xpath("./@href")[0]
        category_url = urljoin(self.main_url, category_url_raw)

        category_name = HtmlElement.xpath("./@title")[0]

        return category_url, category_name
