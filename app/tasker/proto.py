from scraper.helpers.logger import logger
import importlib


class BaseTasker:
    """
    This Tasker loads specified Scrpaer for tracked Website,
        and start needed scraping jobs.
    """

    def __init__(self, module_name, class_name, logger=logger, *args, **kwargs):
        self.logger = logger
        self.module_name = module_name
        self.class_name = class_name

    def get_scraper(self):
        """
        Loads proper Scraper module.
        """
        try:
            module = importlib.import_module(f"scraper.sites.{self.module_name}")
            scraper = getattr(module, f"{self.class_name}")
            self.logger.debug(f"Found Scraper: {self.module_name}.{self.class_name}")
            return scraper
        except ModuleNotFoundError:
            self.logger.error(f"Module was not found: {self.module_name}")

    def scrape_home_page(self, scraper_class, url):
        # TODO:
        # Add integration with HomePage object.
        """"""

        with scraper_class() as scraper:
            response = scraper.selenium_get(url=url)
            element = scraper.parse_response(response=response)
            scraper.close_cookies_banner(element=element)
            new_element = scraper.parse_driver_response()

    # def discover_all_product_pages_for_url(self, scraper_class, url):
    #     """"""

    #     with scraper_class() as scraper:
    #         response = scraper.selenium_get(url=url)
    #         element = scraper.parse_response(response=response)
    #         scraper.close_cookies_banner(element=element)
    #         products = scraper.find_products_for_all_pages_selenium()
    #         for prod in products:
    #             print(prod)
    #         scraper.do_cleanup()
