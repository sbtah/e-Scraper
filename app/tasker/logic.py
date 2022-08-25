"""
Main logic for scraping tasks. Like: discovery of Categories and Products.
Also validation of URLs.
"""

import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


from products.models import Product, ProductLocalData, ProductExtraField
from categories.models import Category
from categories.builders import update_or_create_category
from scraper.logic.medium import EcommerceScraper
from scraper.helpers.logging import logging


class ScrapingTasker(EcommerceScraper):
    """
    Main Class for creating scraping tasks.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def discover_main_categories(self):
        """
        Main discovery process for Categories.
        Given then main URL and Xpath find all main Categories.
        Populate database with URLS/Names.
        """

        element = self.request_url(self.main_url)
        categories = self.extract_urls_with_names(
            html_element=element,
            xpath_to_search=self.main_categories_elements_xpath,
            name_xpath="./@title",
        )
        for category in categories:
            main_category = update_or_create_category(
                current_url=category[0],
                category_name=category[1],
            )
            main_category.category_nesting_level = 1
            main_category.save()

    def discover_child_categories(self, url):
        """
        Discovery process for Child Categories.
        Given the URL and Xpath find all Child Categories of main Category.
        Populate database with URLS/Names.
        """

        element = self.request_url(url)
        try:
            parrent_category = Category.objects.get(current_url=url)

            child_categories = self.extract_urls_with_names(
                html_element=element,
                xpath_to_search=self.child_categories_elements_xpath,
                name_xpath="./@title",
            )
            for category in child_categories:
                print(category)
                child_category = update_or_create_category(
                    current_url=category[0],
                    category_name=category[1],
                )
                child_category.parrent_category = parrent_category
                child_category.category_nesting_level = 2
                child_category.save()
        except Category.DoesNotExist:
            logging.error("No parrent Category with this URL, passing...")

    def discover_all_child_categories(self):
        """
        Discovery process for all Child Categories.
        Given the URLs of main Categories, find all childs.
        Populate database with URLS/Names.
        """

        main_categories = Category.objects.filter(
            category_nesting_level=1,
        )
        for category in main_categories:
            # Request saved URL for Category.
            self.discover_child_categories(category.current_url)

    def scrape_main_categories_data(self):
        """
        Scrape main Categories Data from URLS saved in DB.
        """

        main_categories = Category.objects.filter(
            category_nesting_level=1,
        )
        for category in main_categories:
            # Request saved URL for Category.
            element = self.request_url(category.current_url)
            # If response ...
            if element is not None:
                category.is_active = True
                category.category_description = self.parse_value_from_many_elements(
                    html_element=element,
                    xpath_to_search='.//div[contains(@class, "block-description__text")]',
                    default_on_fail="",
                    value_name="Category Description",
                )
                category.meta_description = self.parse_single_value(
                    html_element=element,
                    xpath_to_search='.//meta[@name="description"]/@content',
                    default_on_fail="",
                    value_name="Category Meta Description",
                )
                category.canonical_url = self.parse_single_value(
                    html_element=element,
                    xpath_to_search='.//link[@rel="canonical"]/@href',
                    default_on_fail="",
                    value_name="Category Canonical URL",
                )
                category.seo_title = self.parse_single_value(
                    html_element=element,
                    xpath_to_search=".//title/text()",
                    default_on_fail="",
                    value_name="Category SEO Title",
                )
                category.save()
                logging.info(f"UPDATED Category: {category.category_name}")
            else:
                logging.error(
                    f"No response for: {category.category_name}, setting Category to inactive..."
                )
