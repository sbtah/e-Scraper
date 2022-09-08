"""
Helper functions for creating or updating new Category objects.
"""
from datetime import datetime
from categories.models import Category
from scraper.helpers.logging import logging


# TODO:
# Add some persistant logging mechanism in second DB.


def update_or_create_category(
    discovery_url,
    category_name,
):
    """
    Create or Update an instance of Category object.
    Used at discovery level, where only Names and Urls are created.
    """
    now = datetime.strptime(
        datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "%d/%m/%Y, %H:%M:%S"
    )
    try:
        category = Category.objects.get(discovery_url=discovery_url)
        if str(category_name) != str(category.category_name):
            category.category_name = category_name
            category.last_discovery = now
            category.save()
            logging.info(f"Found Category, updating name: {category.category_name}")
        else:
            category.last_discovery = now
            category.save()
            logging.info(f"Found Category: {category.category_name}")
    except Category.DoesNotExist:
        category = Category.objects.create(
            discovery_url=discovery_url,
            category_name=category_name,
            last_discovery=now,
        )
        logging.info(f"!! CREATED New Category: {category.category_name}")
    return category
