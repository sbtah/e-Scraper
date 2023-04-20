from scraper.logic.ecommerce import EcommerceScraper
from lxml.html import tostring, HtmlElement
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select


class ScrapingScraper(EcommerceScraper):
    """
    Specialized Scraper that returns data from requested WebPages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def meta_xpath_dict(self):
        """Dictionary of Meta Data Xpathses."""
        return {
            "meta_title_xpath": ".//head/title/text()",
            "meta_description_xpath": './/head/meta[@name="description"]/@content',  # noqa
            "canonical_url_xpath": './/head/link[@rel="canonical"]/@href',
        }

    @property
    def product_page_variants_xpath_dict(self):
        """
        Dictionary of needed Xpathses that triggers ProductData selection of variants on ProductPage.
        Keys are reflecting idea of multiple pickers of variants on ProductPage.
        So for every element in list of buttons / dropdowns produced by key "1",
            - in this dict, picker will click every element in list produced by key "2" and "3".
        We assume 3 is max for now.
        """
        raise NotImplementedError

    def visit_web_page(self, url):
        """
        Requests specified url, closes cookies policy banner.
        Returns dictionary of Meta Data from requested WebPage.
        """

        response = self.selenium_get(url=url)
        element = self.parse_response(response=response)
        meta_data = self.extract_meta_data(html_element=element)
        self.close_cookies_banner(html_element=element)
        return meta_data

    def extract_meta_data(self, html_element):
        """
        Takes HtmlElement.
        Extracts Meta Data from page, explicitly sets each data's type to str.
        Returns dictionary of data that will be used in creation of WebPage objects.
        """
        meta_dict = {}
        try:
            meta_title = html_element.xpath(
                self.meta_xpath_dict.get("meta_title_xpath")
            )[0]
            meta_dict["meta_title"] = str(meta_title)
        except IndexError:
            meta_title = ""
            meta_dict["meta_title"] = str(meta_title)
        except Exception as e:
            self.logger.error(
                f"(exctract_meta_data:meta_title) Some other exception: {e}"
            )
        try:
            meta_description = html_element.xpath(
                self.meta_xpath_dict.get("meta_description_xpath")
            )[0]
            meta_dict["meta_description"] = str(meta_description)
        except IndexError:
            meta_description = ""
            meta_dict["meta_description"] = str(meta_description)
        except Exception as e:
            self.logger.error(
                f"(exctract_meta_data:meta_description) Some other exception: {e}"
            )
        try:
            canonical_url = html_element.xpath(
                self.meta_xpath_dict.get("canonical_url_xpath")
            )[0]
            meta_dict["canonical_url"] = str(canonical_url)
        except IndexError:
            canonical_url = ""
            meta_dict["canonical_url"] = str(canonical_url)
        except Exception as e:
            self.logger.error(
                f"(exctract_meta_data:canonical_url) Some other exception: {e}"
            )
        self.logger.info("Meta Data extracted!")
        return meta_dict

    def activate_product_variants(self, html_element):
        """
        ! This have to be implemented at individual store scraper.
        Given the HtmlElement of ProductPage search for Xpathses,
            used for activation of ProductData variants.
        For every possible combination of variants return HtmlElement.
        """
        raise NotImplementedError

    def extract_product_data(self, html_element):
        product_data = {}
        """
        ! This have to be implemented at individual store scraper.
        Needs to return a dict of values that we want to track,
            - and extract from ProductPage,
        ProductData object will be generated from this data,
            - with fields/values corpesponding key: values in dict.
        """
        raise NotImplementedError

    def scrape_product_page(self, url):
        """
        Visit ProductPage by url.
        Parse each HtmlElement returned by activate_product_variants.
        Returns dictionary of product_page_data which contains meta_data of ProductPage,
            and products_data list of ProductData dictionaries.
        """

        product_page_data = {}
        product_page_data["products_data"] = {}

        meta_data = self.visit_web_page(url=url)
        product_page_data["meta_data"] = meta_data

        element = self.parse_driver_response()
        product_data_elements = self.activate_product_variants(html_element=element)

        for idx, product_element in enumerate(product_data_elements):
            product_page_data["products_data"][idx] = self.extract_product_data(
                html_element=product_element
            )

        return product_page_data

    def extract_home_page_data(self, html_element):
        """"""
        pass

    def extract_category_page_data(self, html_element):
        """"""
        pass

    def extract_blog_page_data(self, html_element):
        """"""
        pass

    def extract_blog_article_page_data(self, html_element):
        """"""
        pass

    def scrape_category_page(self):
        pass
