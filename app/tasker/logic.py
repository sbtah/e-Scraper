"""
Main logic for scraping tasks. Like: discovery or scraping of Categories and Products.
"""

import os
from datetime import datetime, timedelta
import django
from django.db.models import Q


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


from products.models import Product, ProductLocalData, ProductExtraField
from products.builders import discovery_update_or_create_product
from categories.models import Category
from categories.builders import update_or_create_category

from app.scraper.logic.scraper import EcommerceScraper
from scraper.helpers.logging import logging


class ScrapingTasker(EcommerceScraper):
    """
    Main Class for creating scraping tasks.
    """

    def discover_products_for_category(self, id):
        """Discover products for single Category by it's ID."""

        now = datetime.strptime(
            datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "%d/%m/%Y, %H:%M:%S"
        )

        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            logging.error(f"Category with ID:{id} does not exist.")
        else:
            self.discover_products(category.discovery_url)

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
                discovery_url=category[0],
                category_name=category[1],
            )
            main_category.category_nesting_level = 1
            main_category.save()

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
            # Request saved URLS for Category.
            self.discover_child_categories(category.discovery_url)

    def discover_all_sub_categories(self):
        """
        Discovery process for all Sub Categories.
        Given the URLs of Child Categories, find all Subs.
        Populate database with URLS/Names.
        """

        child_categories = Category.objects.filter(
            category_nesting_level=2,
        )
        for category in child_categories:
            # Request saved URLS for Category.
            self.discover_sub_categories(category.discovery_url)

    def discover_child_categories(self, url):
        """
        Discovery process for Child Categories.
        Given the URL and Xpath find all Child Categories of main Category.
        Populate database with URLS/Names.
        """

        element = self.request_url(url)
        current_url = self.driver.current_url
        now = datetime.strptime(
            datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "%d/%m/%Y, %H:%M:%S"
        )

        if current_url == url:
            try:
                parrent_category = Category.objects.get(discovery_url=url)
                child_categories = self.extract_urls_with_names(
                    html_element=element,
                    xpath_to_search=self.child_categories_elements_xpath,
                    name_xpath="./@title",
                )
                logging.info("=" * 48)
                for category in child_categories:
                    child_category = update_or_create_category(
                        discovery_url=category[0],
                        category_name=category[1],
                    )
                    child_category.parrent_category = parrent_category
                    child_category.category_nesting_level = (
                        parrent_category.category_nesting_level + 1
                    )
                    child_category.save()
                parrent_category.related_categories_last_discovery = now
                parrent_category.save()
            except Category.DoesNotExist:
                logging.error("No parrent Category with this URL, passing...")
                pass
        else:
            logging.warning(f"Redirection detected, passing..")
            pass

    def discover_sub_categories(self, url):
        """
        Discovery process for Sub Categories.
        Given the URL and Xpath find all Sub Categories of Child Category.
        Populate database with URLS/Names.
        """

        element = self.request_url(url)
        current_url = self.driver.current_url
        now = datetime.strptime(
            datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "%d/%m/%Y, %H:%M:%S"
        )

        if current_url == url:
            try:
                parrent_category = Category.objects.get(discovery_url=url)
                sub_categories = self.extract_urls_with_names(
                    html_element=element,
                    xpath_to_search='.//h3//a[@class="category-item__name"]',
                    name_xpath="./@title",
                )
                logging.info("=" * 48)
                for category in sub_categories:
                    sub_category = update_or_create_category(
                        discovery_url=category[0],
                        category_name=category[1],
                    )
                    sub_category.parrent_category = parrent_category
                    sub_category.category_nesting_level = (
                        parrent_category.category_nesting_level + 1
                    )
                    sub_category.save()
                parrent_category.related_categories_last_discovery = now
                parrent_category.save()
            except Category.DoesNotExist:
                logging.error("No parrent Category with this URL, passing...")
                pass
        else:
            logging.warning(f"Redirection detected, passing..")
            pass

    def discover_products_for_category(self, url):
        """
        Discovery process for Products.
        Given the Category URL and Xpath find all Products for all pages in Category.
        Populate database with URLS/Names of Products.
        On success flags Category with current date
            - for :related_products_last_discovery: variable.
        """

        element = self.request_url(url)
        current_url = self.driver.current_url
        now = datetime.strptime(
            datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "%d/%m/%Y, %H:%M:%S"
        )

        if current_url == url:
            try:
                parrent_category = Category.objects.get(discovery_url=url)
                products = self.extract_products_from_all_pages(
                    html_element=element,
                )
                logging.info("=" * 48)
                for prod in products:
                    product = discovery_update_or_create_product(
                        discovery_url=prod[0],
                        product_name=prod[1],
                    )
                    parrent_category.products.add(product)
                    try:
                        temp_list = product.parrent_categories.copy()
                        temp_list.append(parrent_category.id)
                        product.parrent_categories = temp_list
                        product.save()
                    except AttributeError:
                        temp_list = []
                        temp_list.append(parrent_category.id)
                        product.parrent_categories = temp_list
                        product.save()
                parrent_category.related_products_last_discovery = now
                parrent_category.save()
            except Category.DoesNotExist:
                logging.error("No parrent Category with this URL, passing...")
                pass
        else:
            logging.warning(f"Redirection detected, passing..")
            pass

    def scrape_main_categories_data(self):
        """
        Scrape main Categories Data from URLS saved in DB.
        """

        main_categories = Category.objects.filter(
            category_nesting_level=1,
        )
        for category in main_categories:
            # Request saved URL for Category.
            element = self.request_url(category.discovery_url)
            # If response ...
            if element is not None:
                category.current_url = self.driver.current_url
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
                category.is_active = False
                category.save()

    def discover_all_products(self):
        """
        Discovery process for all Products.
        Given the URLs of Sub Categories, find all Products.
        Populate database with URLS/Names.
        """
        now = datetime.strptime(
            datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "%d/%m/%Y, %H:%M:%S"
        )
        time_threshold = now - timedelta(days=1)
        sub_categories = Category.objects.filter(
            Q(category_nesting_level=3)
            & (
                Q(related_products_last_discovery__lt=time_threshold)
                | Q(related_products_last_discovery=None)
            )
        )
        for category in sub_categories:
            ## Request saved URLS for Category.
            # print(category.related_products_last_discovery)
            self.discover_products_for_category(category.discovery_url)
