from scraper.logic.scraping_scraper import ScrapingScraper


class MisioHandMade(ScrapingScraper):
    """
    Specialized scraper for Misiohandmade store.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def main_url(self):
        return "https://misioohandmade.pl/"

    @property
    def main_categories_url(self):
        return "https://misioohandmade.pl/sklep/"

    @property
    def terms_and_conditions_url(self):
        return "https://kiddymoon.pl/pl/terms.html"

    @property
    def about_page_url(self):
        return "https://kiddymoon.pl/pl/about/o-nas-94.html"

    @property
    def blog_page_url(self):
        return "https://misioohandmade.pl/blog/"

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
                "category_element_xpath": './/section[contains(@class, "slider")]//div[contains(@class, "swiper-slide")]/a[@class="cat"]',
                "with_child_categories": False,
                "with_products": False,
            },
        }

    def parse_category_level_1_elements(
        self,
        HtmlElement=None,
        SeleniumWebElement=None,
    ):
        # category_url = HtmlElement.xpath("./@href")[0]
        # category_name = HtmlElement.xpath("./h5/text()")[0]
        category_url = SeleniumWebElement.get_attribute("href")
        category_name = SeleniumWebElement.get_attribute("text").strip()
        return category_url, category_name
