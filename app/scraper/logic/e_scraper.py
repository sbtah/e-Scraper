"""
Main logic for scraping tasks. Like: discovery or scraping of Categories and Products.
"""
from app.scraper.logic.scraper import Scraper
from datetime import datetime, timedelta
from django.db.models import Q
from categories.builders import update_or_create_category
from categories.models import Category
from products.builders import discovery_update_or_create_product
from products.models import Product, ProductLocalData, ProductExtraField
from scraper.helpers.logging import logging

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


class EcommerceScraper(Scraper):
    """Main Scraper class that scrapes data to db."""

    pass