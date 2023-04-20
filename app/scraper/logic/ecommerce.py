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
    def main_url(self):
        """Main Url for the tracked Website."""
        raise NotImplementedError

    @property
    def main_categories_url(self):
        """Url from which discovery of CategoryPages is starting."""
        raise NotImplementedError

    @property
    def blog_page_url(self):
        """Url from which discovery of BlogPage is starting."""
        raise NotImplementedError

    @property
    def categories_discovery_xpath_dict(self):
        """
        Dictionary of needed Xpaths and settings for discoverying CategoryPages.
        CategoryPages can have other Categories as a childs.
        Main (root) Categories are mapped to 1 while childs are 2, 3, 4 and so on.

        - :param category_element_xpath: Must return list of Elements to parse.

        return {
            1: {
                "category_element_xpath": None,
            },
        }
        """
        raise NotImplementedError

    @property
    def products_discovery_xpath_dict(self):
        """
        Dictionary of needed Xpaths and settings for discoverying ProductPages.
        ProductsPages are mapped to CategoryPage level by key.

        - :param product_url_xpath: Must return list of Elements to parse.

        return {
            1: {
                "product_url_xpath": "",
                "product_next_page_button_xpath": "",
                "product_current_page_xpath": "",
                "product_last_page_xpath": "",
                "product_previous_page_xpath": "",
            },
        }
        """
        raise NotImplementedError

    def parse_category_level_1_elements(
        self, HtmlElement=None, SeleniumWebElement=None
    ):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: category_page_url, category_page_name
        """
        raise NotImplementedError

    def parse_category_level_2_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: category_page_url, category_page_name
        """
        raise NotImplementedError

    def parse_category_level_3_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: category_page_url, category_page_name
        """
        raise NotImplementedError

    def parse_category_level_4_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: category_page_url, category_page_name
        """
        raise NotImplementedError

    def parse_category_level_5_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: category_page_url, category_page_name
        """
        raise NotImplementedError

    def parse_category_level_6_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: category_page_url, category_page_name
        """
        raise NotImplementedError

    def parse_product_level_1_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: product_page_url, product_page_name
        """
        raise NotImplementedError

    def parse_product_level_2_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: product_page_url, product_page_name
        """
        raise NotImplementedError

    def parse_product_level_3_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: product_page_url, product_page_name
        """
        raise NotImplementedError

    def parse_blog_article_level_1_elements(self, HtmlElement, SeleniumWebElement):
        """
        Needs to be implemented at store Scraper level.
        Takes HtmlElement or SeleniumWebElement, located with find process.
        Parses it and returns URL and Name from it.
        Should return tuple: blog_article_page_url, blog_article_page_name
        """
        raise NotImplementedError

    def extract_urls_with_names(
        self,
        html_element,
        xpath_to_search,
        parser_used=None,
        extract_with_selenium=False,
    ):
        """
        Used in discovery of WebPages Elements on current page.
        Finds all Urls and 'Names' in given HtmlElements.
        Returns generator of tuples, containing (url, name).
        :param xpath_to_search: - Xpath that should return list of HtmlElements
            or SeleniumWebElements.
        :param parser_used: - class method that will extract needed data,
            (URL, Name) from each element in list.
        :param extract_with_selenium: - Default to False means,
            that parsing will expect to work on HtmlElements, while True means,
            that parser have to deal with Selenium Web Element.
        """
        if extract_with_selenium == False:
            categories_list = self.find_all_elements(
                html_element=html_element,
                xpath_to_search=xpath_to_search,
            )
        else:
            categories_list = self.find_selenium_elements(
                xpath_to_search=xpath_to_search,
            )

        if categories_list:
            self.logger.info(
                f"URLS/Names list created, returned {len(categories_list)} elements."  # noqa
            )
            if extract_with_selenium == False:
                return (
                    parser_used(HtmlElement=x, SeleniumWebElement=None)
                    for x in categories_list
                )
            else:
                return (
                    parser_used(SeleniumWebElement=x, HtmlElement=None)
                    for x in categories_list
                )
        else:
            self.logger.info(f"Failed loading URLS/Names list from HTML,")
            return None

    def find_all_category_pages(
        self,
        html_element,
        category_level=1,
        parser_used=None,
        extract_with_selenium=False,
    ):
        """
        Given then HtmlElement.
        Return generator of tuples for CategoryPage: (url, name).
        self.categories_discovery_xpath_dict have to be configured,
            with CategoryPage related xpathses.
        self.categories_discovery_xpath_dict keys are implying CategoryPage level,
            where Root/Main CategoryPage is 1 while childs are 2, 3, 4 and so on.
        :param parser_used:
        :param extract_with_selenium:
            - If set to true data will be extracted with Selenium,
                instead of lxml.
        """
        if (
            self.categories_discovery_xpath_dict.get(category_level)
            and parser_used is not None
        ):
            categories = self.extract_urls_with_names(
                html_element=html_element,
                xpath_to_search=self.categories_discovery_xpath_dict[category_level][
                    "category_element_xpath"
                ],
                parser_used=parser_used,
                extract_with_selenium=extract_with_selenium,
            )
            return categories
        else:
            self.logger.error(
                "(find_all_category_pages) Missing critical Xpathses or CategoryPage parser. Quiting."
            )
            self.do_cleanup()
            return None

    def find_all_product_pages(
        self,
        html_element,
        category_level=1,
        parser_used=None,
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
        if (
            self.products_discovery_xpath_dict.get(category_level)
            and parser_used is not None
        ):
            products = self.extract_urls_with_names(
                html_element=html_element,
                xpath_to_search=self.products_discovery_xpath_dict[category_level][
                    "product_url_xpath"
                ],
                parser_used=parser_used,
                extract_with_selenium=extract_with_selenium,
            )
            return products
        else:
            self.logger.error(
                "(find_all_product_pages) Missing critical Xpathses or ProductPage parser. Quiting."
            )
            self.do_cleanup()
            return None

    def find_product_pages_for_all_pages_selenium(
        self, category_level=1, parser_used=None, extract_with_selenium=False
    ):
        """
        Parses all products for all pages on specified ProductPage.
        Relies on Selenium since it's only clicking next page button.

        To work you need to configure:
        self.products_discovery_xpath_dict

        Returns a generator of tuples with ProductPage data: (url, name).
        """
        if parser_used is not None:
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
                category_level=category_level,
                parser_used=parser_used,
                extract_with_selenium=extract_with_selenium,
            )

            if products is not None:
                for prod in products:
                    yield prod
            else:
                self.logger.error(
                    f"(find_all_product_pages) Returned: '{products}' Products at URL: {self.url} - Quiting."
                )
                pass

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
                    html_element=element,
                    category_level=category_level,
                    parser_used=parser_used,
                    extract_with_selenium=extract_with_selenium,
                )
                if products is not None:
                    for prod in products:
                        yield prod
                else:
                    self.logger.error(
                        f"(find_all_product_pages) Returned: '{products}' Products at URL: {self.url} - Quiting."
                    )
                    pass

            else:
                self.logger.info(
                    "Next page element not found. Parsing products - finished."
                )
        else:
            self.logger.error("Missing ProductPage parser - Quiting.")
            self.do_cleanup()
