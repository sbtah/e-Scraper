from scraper.logic.scraping_scraper import ScrapingScraper
from scraper.helpers.cleaners import extract_price_data


class KiddyMoon(ScrapingScraper):
    """
    Specialized scraper for KiddyMoon store.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        return "https://kiddymoon.pl/"

    @property
    def main_categories_url(self):
        return self.main_url

    @property
    def blog_page_url(self):
        return None

    @property
    def cookies_close_xpath(self):
        return './/button[contains(@id,  "onetrust-accept")]'

    @property
    def categories_discovery_xpath_dict(self):
        return {
            1: {
                "category_element_xpath": './/div[@id="menu_navbar"]/ul/li/a[@class="nav-link" and not(contains(@title, "Nowości")) and not(contains(@title, "O nas")) and not(contains(@title, "Kontakt"))]',
            },
        }

    @property
    def products_discovery_xpath_dict(self):
        return {
            1: {
                "product_url_xpath": './/section[@id="search"]//div[contains(@class, "product") and @data-product_id]/a[@data-product-id]',
                "product_next_page_button_xpath": './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "pagination") and contains(@class, "next") and not(contains(@class, "disabled")) and not(contains(@class, "prev"))]',
                "product_current_page_xpath": './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "--active")]',
                "product_last_page_xpath": './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "pagination") and not(contains(@class, "next")) and not(contains(@class, "prev"))][last()]',
                "product_previous_page_xpath": ".",
            },
        }

    @property
    def product_page_variants_xpath_dict(self):
        return {
            1: {
                "pick_elements": './/div[@id="projector_sizes_cont"]//div[contains(@class, "sizes")]/div/a',
            },
        }

    def extract_product_data(self, html_element):
        product_data = {}
        try:
            # 1
            product_name = html_element.xpath(".//h1/text()")[0]
            product_data["product_name"] = str(product_name)
            self.logger.info(
                f'Found product_name value. Returning: {product_data["product_name"]}'
            )
        except IndexError:
            self.logger.error("Error Xpath returned an empty list. Quiting.")
            self.do_cleanup()
        except Exception as e:
            self.logger.error(
                f"(parse_product_data:product_name) Some other exception: {e}"
            )

            self.do_cleanup()
            # 2
            product_data["product_description"] = (
                html_element.xpath('//section[@id="projector_longdescription"]')[0]
                .text_content()
                .strip()
            )
            # 3
            # extract_price_data
            raw_product_price_for_unit = html_element.xpath(
                './/div[@class="projector_price_subwrapper"]//strong[@id="projector_price_value"]/text()'
            )[0]
            product_data["product_price_for_unit"] = extract_price_data(
                raw_product_price_for_unit
            )
            # 4
            product_data["product_unit_type"] = html_element.xpath(
                './/div[@class="price_gross_info"]//small[@id="projector_price_unit"]/text()'
            )[0]
            # 5
            product_data["product_brand"] = html_element.xpath(
                './/div[contains(@class, "dictionary__param") and .//span[text()="Producent"]]/div[contains(@class, "dictionary__values")]/div[@class="dictionary__value"]/a'
            )
            return product_data

    def parse_category_level_1_elements(
        self,
        HtmlElement,
        SeleniumWebElement,
    ):
        # category_url = HtmlElement.xpath("./@href")[0]
        # category_name = HtmlElement.xpath("./h5/text()")[0]
        category_url = SeleniumWebElement.get_attribute("href")
        category_name = SeleniumWebElement.get_attribute("text").strip()
        return category_url, category_name

    def parse_product_level_1_elements(
        self,
        HtmlElement,
        SeleniumWebElement,
    ):
        product_url = HtmlElement.xpath("./@href")[0]
        product_name = HtmlElement.xpath("./@title")[0]
        # product_url = SeleniumWebElement.get_attribute("href")
        # product_name = SeleniumWebElement.get_attribute("title").strip()
        return product_url, product_name
