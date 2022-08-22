from scraper.helpers import auth
from scraper.helpers.logging import logging
from scraper.logic.basic import BaseScraper
from scraper.helpers.helpers import (
    random_sleep_medium,
    random_sleep_small,
    my_float,
    clean_text,
    clean_stock_text_to_number,
)
from selenium.common.exceptions import (
    ElementNotInteractableException,
)


class EcommerceScraper(BaseScraper):
    def __init__(self, use_python=False, use_selenium=True, *args, **kwargs):
        self.use_selenium = use_selenium
        self.use_python = use_python
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        return auth.MAIN_URL

    @property
    def stores_url(self):
        return auth.STORES_URL

    @property
    def store_picker_top_button_xpath(self):
        return './/button[@name="Wybierz sklep" or @id="shop-selection-master"]'

    @property
    def store_picker_product_site_button_xpath(self):
        return "."

    @property
    def store_picker_first_modal_xpath(self):
        return './/div[@class="base-popup__modal modal"]'

    @property
    def store_picker_first_modal_close_button_xpath(self):
        return '//div[@class="base-popup__modal modal"]//button[@name="Zamknij"]'

    @property
    def store_picker_input_field_start_button_xpath(self):
        return './/button[@class="button-base input-chosen__select-box"]'

    @property
    def store_picker_second_modal_stores_select_xpath(self):
        return './/div[@class="input-chosen__box"]//input'

    @property
    def cookies_policy_close_button(self):
        """Used to find and close cookies policy element."""
        return './/div[@class="cookie-bar__buttons"]//button[@name="Zaakceptuj"]'

    @property
    def main_categories_elements_xpath(self):
        "Used to find all Main Categories on main page."
        return './/a[contains(@class, "categories-menu-recursive-level__link")]'

    @property
    def local_stores_elements_xpath(self):
        """Used on stores sub page."""
        return './/div[@class="row"]//h3//a'

    @property
    def products_elements_xpath(self):
        return './/section[contains(@class, "product-tail products-grid__item")]//h3[contains(@class, "product-tail__name")]//a[contains(@class, "name")]'

    @property
    def product_argument_to_name_xpath(self):
        return "./@title"

    @property
    def product_pages_list_xpath(self):
        return './/ul[contains(@class, "navigation-base")]//li[contains(@class, "base__item")]'

    @property
    def product_next_page_button_xpath(self):
        """"""
        return '//li[contains(@class, "navigation")]//a[contains(@title, "Następna strona")]'

    def pick_store_by_name_top(self, store_name):
        """
        Used to change local stores dynamically.
        It finds 2 modals that have to be initialized.
        Sends value to store name field and sends request to server.
        """
        self.initialize_element(
            xpath_to_click=self.store_picker_top_button_xpath,
            xpath_to_check=self.store_picker_first_modal_xpath,
        )
        self.initialize_element(
            xpath_to_click=self.store_picker_input_field_start_button_xpath,
            xpath_to_check=self.store_picker_second_modal_stores_select_xpath,
        )
        self.send_text_to_input(
            text=store_name,
            xpath_to_find=self.store_picker_second_modal_stores_select_xpath,
        )
        new_html = self.parse_driver_response()
        return new_html

    def close_cookies_policy(self, html_element, xpath_to_search):
        """
        Use with Selenium.
        Used for locating and closing cookies policy element.
        ::param html_element:: HtmlElement
        ::param xpath_to_search::
          Element we want to click in provided HtmlElement.
        """
        element_to_check = self.if_xpath_in_element(
            html_element=html_element, xpath_to_search=xpath_to_search
        )
        logging.info("Found cookies policy element. Closing...")
        if element_to_check is not None:
            close_button = self.return_selenium_element(xpath_to_search=xpath_to_search)
            try:
                close_button.click()
                logging.info("Successfully closed cookies policy element.")
                random_sleep_small()
                html_after_closing = self.parse_driver_response()
                return html_after_closing
            except ElementNotInteractableException:
                logging.info("Can't click on close buton, element was already clicked?")
                html_after_closing = self.parse_driver_response()
                return html_after_closing
        else:
            logging.error(f"Cookies policy element not in the DOM.")
            html_after = self.parse_driver_response()
            return html_after

    def extract_products_urls_with_names(self, html_element):
        """"""
        product_data = self.extract_urls_with_names(
            html_element=html_element,
            xpath_to_search=self.products_elements_xpath,
            name_xpath=self.product_argument_to_name_xpath,
        )
        return product_data

    def extract_products_from_all_pages(self, html_element):
        """
        Works with selenium driver.
        Given the HtmlElement looks for pages number, that have to be parsed.
        Yield Products urls and names for each page.
        Properties must be defined to work:
            -self.cookies_policy_close_button,
            -self.product_next_page_button_xpath,
            -self.product_pages_list_xpath,
            currently works with list...
        """
        # Since I can use this on 1st request I have to be sure we closed cookies banner.
        # I return a fresh HtmlElement anyway...
        element = self.close_cookies_policy(
            html_element=html_element,
            xpath_to_search=self.cookies_policy_close_button,
        )
        # Return list object that I use as an indicator for number of product's pages.
        products_pages_number = self.find_all_elements(
            html_element=element,
            xpath_to_search=self.product_pages_list_xpath,
        )

        # So list can't be empty....
        if products_pages_number:
            # Get the last element of list.
            # This will be a last element with number of max pages in text or value.
            last_page_element = products_pages_number[-1:]
            # Extract number of total pages from element.
            last_page_data = last_page_element[0].xpath(".//a/text()")
            # Clean this data to int.
            last_page_number = int(clean_text(last_page_data[0]))
            total_products_per_category = 0
            for idx, val in enumerate(range(last_page_number)):
                if idx == 0:
                    logging.info(f"First page parsing products...")
                    product_data = self.extract_products_urls_with_names(
                        html_element=element,
                    )
                    for product in product_data:
                        yield product
                else:
                    logging.info(f"Next page parsing products...")
                    next_page_button = self.return_selenium_element(
                        xpath_to_search=self.product_next_page_button_xpath,
                    )
                    next_page_button.click()
                    random_sleep_medium()
                    new_element = self.parse_driver_response()
                    product_data = self.extract_products_urls_with_names(
                        html_element=new_element,
                    )
                    for product in product_data:
                        yield product
        else:
            logging.info(f"No product pages, parsing product from 1st page...")
            product_data = self.extract_products_urls_with_names(
                html_element=element,
            )
            for product in product_data:
                yield product

    ### PRODUCTS ###
    def is_store_picked(self, html_element):
        """
        Checks if store is picked in current product site.
        Used for parsing product's data for certain store.
        """
        element_to_track = './/div[@class="current-market-wrapper"]//button[@name="Wybierz sklep"]/text()'

        try:
            html_element.xpath(element_to_track)[0]
            logging.info("Store Picker element found - store is unpicked.")
            return False
        except IndexError:
            logging.info("Store Picker element not found - store is picked.")
            return True

    def parse_product_single_value(
        self,
        html_element,
        xpath_to_search,
        default_on_fail,
        value_name,
    ):
        """
        Used when data is in single HtmlElement.
        Given the HtmlElement return Product's needed value by Xpath.
        """
        if (
            self.if_xpath_in_element(
                xpath_to_search=xpath_to_search,
                html_element=html_element,
            )
            is not None
        ):
            product_value = html_element.xpath(xpath_to_search)[0].strip()
        else:
            logging.error(f"XPATH for: '{value_name}' Failed...")
            product_value = default_on_fail

        return product_value

    def parse_product_list_values(
        self,
        html_element,
        xpath_to_search,
        default_on_fail,
        value_name,
    ):
        """
        Used when data is in list HtmlElements.
        Given the HtmlElements return Product's needed values by Xpath.
        """
        if (
            self.if_xpath_in_element(
                xpath_to_search=xpath_to_search,
                html_element=html_element,
            )
            is not None
        ):
            product_values = html_element.xpath(xpath_to_search)
        else:
            logging.error(f"XPATH for: '{value_name}' Failed...")
            product_values = default_on_fail

        return product_values

    def parse_product_value_from_many_elements(
        self,
        html_element,
        xpath_to_search,
        default_on_fail,
        value_name,
    ):
        """
        Used when data is in many HtmlElements (like description...) and we want to extract text...
        Given the HtmlElements return Product's needed text by Xpath.
        """
        if (
            self.if_xpath_in_element(
                xpath_to_search=xpath_to_search,
                html_element=html_element,
            )
            is not None
        ):
            product_value = (
                html_element.xpath(xpath_to_search)[0].text_content().strip()
            )
        else:
            logging.error(f"XPATH for: '{value_name}' Failed...")
            product_value = default_on_fail

        return product_value

    def parse_product_page(
        self,
        element_to_parse,
    ):
        """
        Parses product's HTMLelement.
        Finds needed values by Xpath.
        Returns a dictionary of all values that we want to track.

        Parses data only if store is picked!

        Values tracked:
        current_url,
        product_name,
        produc_brand,
        product_sku,
        product_description,
        product_price_for_unit,
        product_price_for_piece,
        product_price_before_promo,
        product_traits,
        is_in_promo,
        """

        # TODO:
        # Since we can access product url directly we have to be sure that we closed a cookies modal ? (if needed? Data is getting parsed by XPATH...)
        # Check for store to be picked on product page. Other wise data is useless.
        store_picked = self.is_store_picked(element_to_parse)

        if store_picked:
            logging.info("=" * 48)
            logging.info("Parsing Product Data...")

            # Main Bar DATA
            current_url = element_to_parse.base_url
            product_name = element_to_parse.xpath(".//h1/text()")[0].strip()

            ### PRODUCT Brand.
            # NOT ALL PRODUCTS HAVE A BRAND.
            product_brand = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//div[contains(@class, "product-content-header__brand")]//span[contains(@class, "brand-text")]/following-sibling::a[contains(@class, "brand-link")]/text()',
                default_on_fail="",
                value_name="Product Brand",
            )

            ### PRODUCT Sku
            product_sku = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//div[contains(@class, "product-content-header__brand")]//span[@class="product-content-header__product-sku"]//span/text()',
                default_on_fail="",
                value_name="Product SKU",
            )

            ### PRODUCT Description
            product_description = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//div[@class="product-main-data__description"]/text()',
                default_on_fail="",
                value_name="Product Description",
            )

            ### PRODUCT Traits.
            product_traits = self.parse_product_list_values(
                html_element=element_to_parse,
                xpath_to_search='.//ul[@class="product-main-data__benefits product-benefits"]//li[@class="product-benefits__item"]/text()',
                default_on_fail=[],
                value_name="Product Traits",
            )

            ### PRODUCT PROMO Type
            product_promo_type = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//section[contains(@class, "product-main-data")]//div[contains(@class, "product-labels")]//a[not(@title="nowość")]/span/text()',
                default_on_fail="",
                value_name="Product Promo Type",
            )

            ### Side Bar DATA ###
            ### PRODUCT PRICE FOR Unit.
            product_price_for_unit = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//section[contains(@class, "product-page-price-box")]//span[@test-id="pageProductPriceBoxValue"]/text()',
                default_on_fail=0,
                value_name="Product Price for Unit",
            )

            ### PRODUCT UNIT Type
            product_unit_type = self.parse_product_value_from_many_elements(
                html_element=element_to_parse,
                xpath_to_search='.//section[contains(@class, "product-page-price-box")]//span[@class="price-unit price-unit--product-page-price-box"]',
                default_on_fail="",
                value_name="Product Unit Type",
            )

            ### PRODUCT PRICE FOR Piece
            product_price_for_piece = self.parse_product_value_from_many_elements(
                html_element=element_to_parse,
                xpath_to_search='.//span[contains(@class, "conversion-info__price-value")]',
                default_on_fail=0,
                value_name="Product Price For Piece",
            )

            ### PRODUCT PIECE Type.
            product_piece_type = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//span[@class="price-unit"]/text()',
                default_on_fail="",
                value_name="Product Piece Type",
            )

            ## PRODUCT PRICE BEFORE Promo.
            product_price_before_promo = self.parse_product_value_from_many_elements(
                html_element=element_to_parse,
                xpath_to_search='.//span[contains(@class, "price-value") and contains(@class, "old-value")]',
                default_on_fail=0,
                value_name="Product Price Before Promo",
            )

            ### Aditional Info DATA ###
            ### PRODUCT WARRANTY Time.
            product_warranty_time = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//h3[contains(text(), "indywidualne")]/following-sibling::table//tr/child::td[contains(text(), "Gwarancja")]/following-sibling::td/text()',
                default_on_fail="",
                value_name="Product Warranty Time",
            )

            ### PRODUCT EAN Code.
            product_ean = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//h3[contains(text(), "indywidualne")]/following-sibling::table//tr/child::td[contains(text(), "EAN")]/following-sibling::td/text()',
                default_on_fail="",
                value_name="Product Ean",
            )

            ### PRODUCT Availability.
            product_availability = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//div[contains(@class, "product-page-sidebar")]//span[contains(@class, "availability-text")]/text()',
                default_on_fail="",
                value_name="Product Availability",
            )

            ### PRODUCT CURRENT Stock.
            product_current_stock = self.parse_product_single_value(
                html_element=element_to_parse,
                xpath_to_search='.//div[contains(@class, "product-page-sidebar")]//span[contains(@class, "product-quantity-text")]/text()',
                default_on_fail="",
                value_name="Product Current Stock",
            )
            print(
                {
                    "current_url": current_url,
                    "product_name": product_name,
                    "product_brand": product_brand,
                    "product_sku": product_sku,
                    "product_description": product_description,
                    "product_traits": product_traits,
                    "product_promo_type": product_promo_type,
                    # Side Bar
                    "product_price_for_unit": my_float(product_price_for_unit),
                    "product_unit_type": clean_text(product_unit_type),
                    "product_price_for_piece": my_float(product_price_for_piece),
                    "product_piece_type": product_piece_type,
                    "product_price_before_promo": my_float(product_price_before_promo),
                    # Aditional Info
                    "product_warranty_time": product_warranty_time,
                    "product_ean": product_ean,
                    "product_availability": product_availability,
                    "product_current_stock": clean_stock_text_to_number(
                        product_current_stock,
                    ),
                }
            )
            return {
                "current_url": current_url,
                "product_name": product_name,
                "product_brand": product_brand,
                "product_sku": product_sku,
                "product_description": product_description,
                "product_traits": product_traits,
                "product_promo_type": product_promo_type,
                # Side Bar
                "product_price_for_unit": my_float(product_price_for_unit),
                "product_unit_type": clean_text(product_unit_type),
                "product_price_for_piece": my_float(product_price_for_piece),
                "product_piece_type": product_piece_type,
                "product_price_before_promo": my_float(product_price_before_promo),
                # Aditional Info
                "product_warranty_time": product_warranty_time,
                "product_ean": product_ean,
                "product_availability": product_availability,
                "product_current_stock": clean_stock_text_to_number(
                    product_current_stock,
                ),
            }
        else:
            logging.info(f"Store is not picked for: {self.driver.current_url}")
            pass
