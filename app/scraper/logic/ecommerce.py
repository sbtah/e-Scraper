import time

from scraper.helpers.randoms import (
    random_sleep_medium,
    random_sleep_small,
    random_sleep_small_l2,
)
from scraper.logic.base import BaseScraper


class EcommerceScraper(BaseScraper):
    """
    General Discovery Scraper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def categories_discovery_xpath_dict(self):
        """
        Dictionary of needed Xpaths and settings for discoverying CategoryPages.
        CategoryPages can have other Categories as a childs.
        Main (root) Categories are mapped to 1 while childs are 2, 3, 4 and so on.
        :param category_url_xpath: Must return enitre <a> tag.
        :param category_name_xpath: Is used for extracting CategoryPage name from Url.
        """
        return {
            1: {
                "category_url_xpath": "",
                "category_name_xpath": "",
                "with_child_categories": False,
                "with_products": False,
            },
        }

    @property
    def products_discovery_xpath_dict(self):
        """
        Dictionary of needed Xpaths and settings for discoverying ProductPages.
        ProductsPages are mapped to CategoryPage level by key.
        :param product_url_xpath: Must return enitre <a> tag.
        :param product_name_xpath: Is used for extracting ProductPage name from Url.
        """
        return {
            1: {
                "product_url_xpath": "",
                "product_name_xpath": "",
                "product_next_page_button_xpath": "",
                "product_current_page_xpath": "",
                "product_last_page_xpath": "",
                "product_previous_page_xpath": "",
            },
        }

    def find_all_category_pages(
        self,
        html_element,
        category_level=1,
        extract_with_selenium=False,
    ):
        """
        Given then HtmlElement.
        Return generator of tuples for CategoryPage: (url, name).
        self.categories_discovery_xpath_dict have to be configured,
            with CategoryPage related xpathses.
        self.categories_discovery_xpath_dict keys are implying CategoryPage level,
            where Root/Main CategoryPage is 1 while childs are 2, 3, 4 and so on.

        :param extract_with_selenium:
            - If set to true data will be extracted with Selenium,
                instead of lxml.
        """
        if self.categories_discovery_xpath_dict.get(category_level):
            if extract_with_selenium:
                categories = self.extract_urls_with_names_selenium(
                    xpath_to_search=self.categories_discovery_xpath_dict[
                        category_level
                    ]["category_url_xpath"],
                    name_attr=self.categories_discovery_xpath_dict[category_level][
                        "category_name_xpath"
                    ],
                )
                return categories
            else:
                categories = self.extract_urls_with_names(
                    html_element=html_element,
                    xpath_to_search=self.categories_discovery_xpath_dict[
                        category_level
                    ]["category_url_xpath"],
                    name_attr_xpath=self.categories_discovery_xpath_dict[
                        category_level
                    ]["category_name_xpath"],
                )
                return categories
        else:
            self.logger.error("(find_all_category_pages) Missing critical Xpathses.")
            return None

    def find_all_product_pages(
        self,
        html_element,
        category_level=1,
        extract_with_selenium=False,
    ):
        """
        Given then HtmlElement.
        Return generator of tuples for ProductPage: (url, name).
        self.products_discovery_xpath_dict have to be configured,
            with ProductPage related xpathses.

        Sometimes products can be displayed differently on different CategoryPage.
        :param category_level: is used here to link ProductPages Xpathses with proper category.

        For instance: If child category (level=2) is displaying product data, then we fetch
            self.products_discovery_xpath_dict for key '2' in dictionary of Xpathses.

        :param extract_with_selenium:
            - If set to true data will be extracted with Selenium,
                instead of lxml.
        """
        if self.products_discovery_xpath_dict.get(category_level):
            if extract_with_selenium:
                products = self.extract_urls_with_names_selenium(
                    xpath_to_search=self.products_discovery_xpath_dict[category_level][
                        "product_url_xpath"
                    ],
                    name_attr=self.products_discovery_xpath_dict[category_level][
                        "product_name_xpath"
                    ],
                )
                return products
            else:
                products = self.extract_urls_with_names(
                    html_element=html_element,
                    xpath_to_search=self.products_discovery_xpath_dict[category_level][
                        "product_url_xpath"
                    ],
                    name_attr_xpath=self.products_discovery_xpath_dict[category_level][
                        "product_name_xpath"
                    ],
                )
                return products
        else:
            self.logger.error("(find_all_product_pages) Missing critical Xpathses.")
            return None

    def find_product_pages_for_all_pages_selenium(
        self, category_level=1, extract_with_selenium=False
    ):
        """
        Parses all products for all pages on specified ProductPage.
        Relies on Selenium since it's only clicking next page button.

        To work you need to configure:
        self.products_discovery_xpath_dict

        Returns a generator of tuples with ProductPage data: (url, name).
        """

        current_page = 1
        element = self.parse_driver_response()
        current_page_number_from_xpath = self.find_all_elements(
            html_element=element,
            # Current page Xpath
            xpath_to_search=self.products_discovery_xpath_dict[category_level][
                "product_current_page_xpath"
            ],
            ignore_not_found_errors=True,
        )
        self.logger.info(
            f"Current page; XPath: {current_page_number_from_xpath[0].text_content().strip() if current_page_number_from_xpath != None else 1} Counted: {current_page}"
        )

        products = self.find_all_product_pages(
            html_element=element,
            extract_with_selenium=extract_with_selenium,
        )

        if products is not None:
            for prod in products:
                yield prod
        else:
            self.logger.error(f"(find_all_product_pages) Returned: {products} Quiting.")
            self.do_cleanup()

        next_page_button = self.find_selenium_element(
            # Next Page Xpath
            xpath_to_search=self.products_discovery_xpath_dict[category_level][
                "product_next_page_button_xpath"
            ],
            ignore_not_found_errors=True,
        )
        while next_page_button is not None:

            self.logger.info(f"Found another product page, proceeding.")
            self.initialize_html_element(next_page_button)
            next_page_button = self.find_selenium_element(
                # Next Page Xpath
                xpath_to_search=self.products_discovery_xpath_dict[category_level][
                    "product_next_page_button_xpath"
                ],
                ignore_not_found_errors=True,
            )

            current_page += 1
            new_element = self.parse_driver_response()
            current_page_number_from_xpath = self.find_all_elements(
                html_element=new_element,
                # Current Page Xpath
                xpath_to_search=self.products_discovery_xpath_dict[category_level][
                    "product_current_page_xpath"
                ],
                ignore_not_found_errors=True,
            )
            self.logger.info(
                f"Current page; XPath: {current_page_number_from_xpath[0].text_content().strip() if current_page_number_from_xpath != None else 1} Counted: {current_page}"
            )

            products = self.find_all_product_pages(
                html_element=element, extract_with_selenium=extract_with_selenium
            )
            if products is not None:
                for prod in products:
                    yield prod
            else:
                self.logger.error(
                    f"(find_all_product_pages) Returned: {products} Quiting."
                )
                self.do_cleanup()

        else:
            self.logger.info(
                "Next page element not found. Parsing products - finished."
            )
