from scraper.logic.ecommerce import EcommerceScraper
from scraper.helpers.logging import logging


class Castorama(EcommerceScraper):
    """
    Specialized scraper for KiddyMoon store.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        return "https://www.castorama.pl/"

    @property
    def main_categories_xpath(self):
        return './/ul[contains(@class, "categories-menu")]//li[.//a]/a'

    @property
    def cookies_close_xpath(self):
        return './/button[@name="Zaakceptuj"]'

    @property
    def all_products_xpath(self):
        """Xpath that returns list of all product's <a> tags."""
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
