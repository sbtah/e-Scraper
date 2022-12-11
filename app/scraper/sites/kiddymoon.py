from scraper.logic.scraping_scraper import ScrapingScraper


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
    def terms_and_conditions_url(self):
        return "https://kiddymoon.pl/pl/terms.html"

    @property
    def about_page_url(self):
        return "https://kiddymoon.pl/pl/about/o-nas-94.html"

    @property
    def blog_page_url(self):
        return None

    @property
    def cookies_close_xpath(self):
        return './/button[contains(@id,  "onetrust-accept")]'

    @property
    def home_page_xpath_dict(self):
        return {
            "main_title": "",
            "main_description": "",
        }

    @property
    def categories_discovery_xpath_dict(self):
        return {
            1: {
                "category_element_xpath": './/div[@id="menu_navbar"]/ul/li/a[@class="nav-link" and not(contains(@title, "Nowości")) and not(contains(@title, "O nas")) and not(contains(@title, "Kontakt"))]',
                "with_child_categories": False,
                "with_products": False,
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
        # product_url = HtmlElement.xpath("./@href")[0]
        # product_name = HtmlElement.xpath("./@title")[0]
        product_url = SeleniumWebElement.get_attribute("href")
        product_name = SeleniumWebElement.get_attribute("title").strip()
        return product_url, product_name
