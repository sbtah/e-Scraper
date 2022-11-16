from scraper.logic.ecommerce import EcommerceScraper
from scraper.helpers.logging import logging


class KiddyMoon(EcommerceScraper):
    """
    Specialized scraper for KiddyMoon store.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        """Main url of site from which scraping will start."""
        return "https://kiddymoon.pl/"

    @property
    def main_categories_xpath(self):
        return './/nav[@id="menu_categories"]//div[@id="menu_navbar"]//ul[contains(@class, "navbar-nav")]/li/a[not(contains(@title, "O nas")) and not(contains(@title, "Kontakt"))]'

    @property
    def cookies_close_xpath(self):
        return './/button[contains(@id,  "onetrust-accept")]'

    @property
    def all_products_xpath(self):
        return './/section[@id="search"]//div[contains(@class, "product") and @data-product_id]/a[@data-product-id]'

    @property
    def products_names_attribute_xpath(self):
        """Xpath that product's name from url. Example: text(), or @title"""
        return "./@title"

    @property
    def current_product_page_xpath(self):
        return './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "--active")]'

    @property
    def last_product_page_xpath(self):
        """Explicit Xpath that returns value of last product page"""
        return './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "pagination") and not(contains(@class, "next")) and not(contains(@class, "prev"))][last()]'

    @property
    def next_product_page_button_xpath(self):
        """Xpath that returns selenium webelement to be clicked."""
        return './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "pagination") and contains(@class, "next") and not(contains(@class, "disabled")) and not(contains(@class, "prev"))]'
