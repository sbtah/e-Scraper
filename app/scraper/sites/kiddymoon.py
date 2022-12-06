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
                "category_url_xpath": './/div[@id="menu_navbar"]/ul/li/a[@class="nav-link" and not(contains(@title, "Nowości")) and not(contains(@title, "O nas")) and not(contains(@title, "Kontakt"))]',
                "category_name_xpath": "./@title",
                "with_products": False,
            },
        }

    @property
    def products_discovery_xpath_dict(self):
        return {
            1: {
                "product_url_xpath": './/section[@id="search"]//div[contains(@class, "product") and @data-product_id]/a[@data-product-id]',
                "product_name_xpath": "./@title",
                "product_next_page_button_xpath": './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "pagination") and contains(@class, "next") and not(contains(@class, "disabled")) and not(contains(@class, "prev"))]',
                "product_current_page_xpath": './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "--active")]',
                "product_last_page_xpath": './/div[@id="paging_setting_bottom"]//ul[contains(@class, "pagination")]//li[contains(@class, "pagination") and not(contains(@class, "next")) and not(contains(@class, "prev"))][last()]',
                "product_previous_page_xpath": ".",
            },
        }
