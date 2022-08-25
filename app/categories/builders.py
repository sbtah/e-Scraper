"""
Helper functions for creating or updating new Category objects.
"""
from categories.models import Category
from scraper.helpers.logging import logging


# TODO:
# Add some persistand logging mechanism in second DB.


def update_or_create_category(
    current_url,
    category_name,
):
    """Create or Update an instance of Category object."""

    try:
        category = Category.objects.get(current_url=current_url)

        if str(category_name) != str(category.category_name):
            category.current_url = current_url
            category.category_name = category_name
            category.save()
            logging.info(f"!! UPDATE Category: {category.category_name}")
        else:
            logging.info(f"NO UPDATES for Category: {category.category_name}")
    except Category.DoesNotExist:
        category = Category.objects.create(
            current_url=current_url,
            category_name=category_name,
        )
        logging.info(f"!! CREATE Category: {category.category_name}")

    return category
