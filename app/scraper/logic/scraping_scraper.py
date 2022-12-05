from scraper.logic.ecommerce import EcommerceScraper


class ScrapingScraper(EcommerceScraper):
    """
    Specialized Scraper that returns data from requested WebPages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        """Main url of tracked site leading to HomePage."""
        return ""

    @property
    def meta_xpath_dict(self):
        """Dictionary of Meta Data Xpathses."""
        return {
            "meta_title_xpath": ".//head/title/text()",
            "meta_description_xpath": './/head/meta[@name="description"]/@content',  # noqa
            "canonical_url_xpath": './/head/link[@rel="canonical"]/@href',
        }

    @property
    def home_page_xpath_dict(self):
        """Dictionary of needed Xpathses for HomePage."""
        return {
            "main_title": "",
            "main_description": "",
        }

    def visit_web_page(self, url):
        """
        Requests specified url, closes cookies policy banner.
        Returns dictionary of Meta Data from requested WebPage.
        """

        response = self.selenium_get(url=url)
        element = self.parse_response(response=response)
        meta_data = self.extract_meta_data(html_element=element)
        self.close_cookies_banner(element=element)
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

    def extract_home_page_data(self, html_element):
        """"""
        pass

    def extract_category_page_data(self, html_element, category_level):
        """"""
        pass

    def extract_product_page_data(self, html_element):
        """"""
        pass

    def extract_product_data(self, html_element):
        """"""
        pass

    def extract_about_page_data(self, html_element):
        """"""
        pass

    def extract_blog_page_data(self, html_element):
        """"""
        pass

    def extract_blog_article_page_data(self, html_element):
        """"""
        pass

    def scrape_home_page(self, root_categories_on_home=True):
        """
        Request Website by self.main_url.
        Returns dictionary of data for HomePage object.
        """
        home_page_dict = {}

        meta_data = self.visit_web_page(url=self.main_url)
        element = self.parse_driver_response()
        home_page_dict["meda_data"] = meta_data
        # TODO :
        # ADD Extracting of HomePage data

        return home_page_dict
