from scraper.helpers.logging import logging
from scraper.helpers.randoms import (
    random_sleep_medium,
    random_sleep_small,
    random_sleep_small_l2,
)
from scraper.logic.base import BaseScraper
import time


class EcommerceScraper(BaseScraper):
    """
    General Ecommerce Scraper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        """Main url of tracked site."""
        return ""

    @property
    def main_categories_xpath(self):
        """Should return Xpath that will return list of <a> tags."""
        return ""

    @property
    def all_products_xpath(self):
        """Xpath that returns list of all product's <a> tags."""
        return ""

    @property
    def products_names_attribute_xpath(self):
        """Xpath that product's name from url. Example: text(), or @title"""
        return ""

    @property
    def products_names_attribute_name(self):
        """
        Attribute for product name from url. Example: text, or title
        Used with selenium webelements.
        """
        return ""

    @property
    def current_product_page_xpath(self):
        """Explicit Xpath that returns value of current product page"""
        return ""

    @property
    def last_product_page_xpath(self):
        """Explicit Xpath that returns value of last product page"""
        return ""

    @property
    def next_product_page_button_xpath(self):
        """Explicit Xpath that returns value of last product page"""
        return ""

    @property
    def cookies_close_xpath(self):
        """Xpath to element that closes cookies banner on click."""
        return ""

    def close_cookies_banner(self, element):
        """"""
        self.close_selenium_element(
            element=element,
            xpath_to_search=self.cookies_close_xpath,
        )

    def close_selenium_element(self, element, xpath_to_search):
        """"""
        if_banner_in_html = self.if_xpath_in_element(
            html_element=element, xpath_to_search=xpath_to_search
        )
        if if_banner_in_html:
            logging.info("WebElement found, closing...")
            try:
                cookies_close_button = self.find_selenium_element(
                    xpath_to_search=xpath_to_search
                )
                self.initialize_html_element(cookies_close_button)
                logging.info("Successfully closed WebElement.")
            except Exception as e:
                logging.error(f"(close_selenium_element) Some other exception: {e}")
        else:
            logging.info("No WebElement to click, passing...")

    def find_all_products(self, html_element):
        """
        Given then HtmlElement.
        Return generator of tuples for product's (url, name).
        You need to configure:
        self.all_products_xpath,
        self.product_names_attribute_xpath.
        """
        if self.all_products_xpath and self.products_names_attribute_xpath:
            products = self.extract_urls_with_names(
                html_element=html_element,
                xpath_to_search=self.all_products_xpath,
                name_attr_xpath=self.products_names_attribute_xpath,
            )
            return products
        else:
            logging.error("(find_all_products) Missing critical Xpathses.")
            return None

    def find_products_for_all_pages_selenium(self):
        """
        Parse all products for all pages in specified page.
        Relies on Selenium since it's only clicking on next page button.
        To work you need to configure:
        self.all_products_xpath,
        self.product_names_attribute_xpath,
        self.current_product_page_xpath,
        self.next_product_page_button_xpath

        Produces a generator of tuples with Product (url, name).
        """

        current_page = 1
        element = self.parse_driver_response()
        current_page_number_from_xpath = self.find_all_elements(
            html_element=element,
            xpath_to_search=self.current_product_page_xpath,
            ignore_not_found_errors=True,
        )
        logging.info(
            f"Current page; XPath: {current_page_number_from_xpath[0].text_content().strip() if current_page_number_from_xpath != None else 1} Counted: {current_page}"
        )

        products = self.find_all_products(html_element=element)
        for prod in products:
            yield prod

        next_page_button = self.find_selenium_element(
            xpath_to_search=self.next_product_page_button_xpath,
            ignore_not_found_errors=True,
        )
        while next_page_button is not None:

            logging.info(f"Found another product page, proceeding.")
            self.initialize_html_element(next_page_button)
            next_page_button = self.find_selenium_element(
                xpath_to_search=self.next_product_page_button_xpath,
                ignore_not_found_errors=True,
            )

            current_page += 1
            new_element = self.parse_driver_response()
            current_page_number_from_xpath = self.find_all_elements(
                html_element=new_element,
                xpath_to_search=self.current_product_page_xpath,
                ignore_not_found_errors=True,
            )
            logging.info(
                f"Current page; XPath: {current_page_number_from_xpath[0].text_content().strip() if current_page_number_from_xpath != None else 1} Counted: {current_page}"
            )

            products = self.find_all_products(html_element=element)
            for prod in products:
                yield prod

        else:
            logging.info("Next page element not found. Parsing products - finished.")
