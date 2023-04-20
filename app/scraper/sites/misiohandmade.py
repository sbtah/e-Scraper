from scraper.logic.scraping_scraper import ScrapingScraper
from scraper.helpers.randoms import random_sleep_small


class MisiooHandMade(ScrapingScraper):
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
    def blog_page_url(self):
        return "https://misioohandmade.pl/blog/"

    @property
    def cookies_close_xpath(self):
        return './/button[contains(@id,  "onetrust-accept")]'

    @property
    def potenial_popups_xpaths(self):
        return ['.//div[@class="popup anim visible"]//span[@class="popup__close"]']

    @property
    def categories_discovery_xpath_dict(self):
        return {
            1: {
                "category_element_xpath": './/section[contains(@class, "slider")]//div[contains(@class, "swiper-slide")]/a[@class="cat"]',
            },
        }

    @property
    def products_discovery_xpath_dict(self):
        return {
            1: {
                "product_url_xpath": './/div[contains(@class, "products")]/div[contains(@class, "card product")]',
                "product_next_page_button_xpath": './/nav[@class="pagination"]/div[./a[contains(@class,  "next")]]',
                "product_current_page_xpath": './/nav[@class="pagination"]/div[./span[contains(@class, "current")]]/span',
                "product_last_page_xpath": "",
                "product_previous_page_xpath": "",
            },
        }

    @property
    def product_page_variants_xpath_dict(self):
        return {
            1: {
                "pick_elements": './/div[contains(@class, "single-product__variations")]//select[contains(@id, "pa")][1]/option[not(contains(text(), "Wybierz"))]/text()',
                "activate_xpath": './/div[contains(@class, "single-product__variations")]//select[contains(@id, "pa")][1]',
            },
            2: {
                "pick_elements": './/div[contains(@class, "single-product__variations")]//select[contains(@id, "pa")][2]/option[not(contains(text(), "Wybierz"))]/text()',
                "activate_xpath": './/div[contains(@class, "single-product__variations")]//select[contains(@id, "pa")][2]',
            },
        }

    def activate_product_variants(self, html_element):

        html_elements = []

        if_variant_picker_1 = self.if_xpath_in_element(
            html_element=html_element,
            xpath_to_search=self.product_page_variants_xpath_dict[1]["activate_xpath"],
        )
        if_variant_picker_2 = self.if_xpath_in_element(
            html_element=html_element,
            xpath_to_search=self.product_page_variants_xpath_dict[2]["activate_xpath"],
        )
        if if_variant_picker_1 and if_variant_picker_2:
            self.logger.info(
                "Parsing ProductData variants. Both picker elements found."
            )
            buttons_text_1 = self.find_all_elements(
                html_element=html_element,
                xpath_to_search=self.product_page_variants_xpath_dict.get(1).get(
                    "pick_elements"
                ),
            )
            buttons_text_2 = self.find_all_elements(
                html_element=html_element,
                xpath_to_search=self.product_page_variants_xpath_dict.get(2).get(
                    "pick_elements"
                ),
            )

            select_1 = self.find_selenium_select_element(
                xpath_to_search=self.product_page_variants_xpath_dict[1][
                    "activate_xpath"
                ]
            )

            select_2 = self.find_selenium_select_element(
                xpath_to_search=self.product_page_variants_xpath_dict[2][
                    "activate_xpath"
                ]
            )

            for b_1 in buttons_text_1:
                self.logger.info(f"Selecting 1st selector: value: {b_1}")
                select_1.select_by_visible_text(b_1)
                random_sleep_small()
                for b_2 in buttons_text_2:
                    select_2.select_by_visible_text(b_2)
                    self.logger.info(
                        f"Selecting 2nd selector: value: {b_2} for 1st selector: {b_1}"
                    )
                    random_sleep_small()
                    self.close_popups_elements_on_error(
                        xpathses_to_search=self.potenial_popups_xpaths
                    )
                    html_elem = self.parse_driver_response()
                    html_elements.append(html_elem)

        elif if_variant_picker_1 and not if_variant_picker_2:
            self.logger.info("Parsing ProductData variants. Only picker 1 was found.")
            buttons_text_1 = self.find_all_elements(
                html_element=html_element,
                xpath_to_search=self.product_page_variants_xpath_dict.get(1).get(
                    "pick_elements"
                ),
            )
            select_1 = self.find_selenium_select_element(
                xpath_to_search=self.product_page_variants_xpath_dict[1][
                    "activate_xpath"
                ]
            )
            for b_1 in buttons_text_1:
                self.logger.info(f"Selecting 1st selector: value: {b_1}")
                select_1.select_by_visible_text(b_1)
                random_sleep_small()
                self.close_popups_elements_on_error(
                    xpathses_to_search=self.potenial_popups_xpaths
                )
                html_elem = self.parse_driver_response()
                html_elements.append(html_elem)

        elif if_variant_picker_2 and not if_variant_picker_1:
            self.logger.info("Parsing ProductData variants. Only picker 2 was found.")
            buttons_text_2 = self.find_all_elements(
                html_element=html_element,
                xpath_to_search=self.product_page_variants_xpath_dict.get(2).get(
                    "pick_elements"
                ),
            )
            select_2 = self.find_selenium_select_element(
                xpath_to_search=self.product_page_variants_xpath_dict[2][
                    "activate_xpath"
                ]
            )
            for b_2 in buttons_text_2:
                self.logger.info(f"Selecting 2nd selector: value: {b_2}")
                select_2.select_by_visible_text(b_2)
                random_sleep_small()
                self.close_popups_elements_on_error(
                    xpathses_to_search=self.potenial_popups_xpaths
                )
                html_elem = self.parse_driver_response()
                html_elements.append(html_elem)
        else:
            self.logger.info(
                "Parsing ProductData variants. No variants pickers were found."
            )
            self.close_popups_elements_on_error(
                xpathses_to_search=self.potenial_popups_xpaths
            )
            html_elem = self.parse_driver_response()
            html_elements.append(html_elem)

        return html_elements

    def extract_product_data(self, html_element):
        product_data = {}

        product_name = self.find_element(
            html_element=html_element,
            xpath_to_search=".//h1/text()",
        )
        product_data["product_name"] = product_name

        return product_data

    def parse_category_level_1_elements(
        self,
        HtmlElement,
        SeleniumWebElement,
    ):
        category_url = HtmlElement.xpath("./@href")[0]
        category_name = HtmlElement.xpath("./h5/text()")[0]
        return category_url, category_name

    def parse_product_level_1_elements(
        self,
        HtmlElement,
        SeleniumWebElement,
    ):
        product_url = HtmlElement.xpath(
            './div[@class="card__hover"]/a[contains(@class, "product__link")]/@href'
        )[0]
        product_name = HtmlElement.xpath(
            './h2[contains(@class, "product__title")]/text()'
        )[0]
        return product_url, product_name
