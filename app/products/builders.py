"""
Helper functions for creating or updating new Product objects.
"""
from datetime import datetime
from products.models import Product
from scraper.helpers.logging import logging


# TODO:
# Add some persistant logging mechanism in second DB.


def discovery_update_or_create_product(
    discovery_url,
    product_name,
):
    """
    Create or Update an instance of Product object.
    Used at discovery level, where only Names and Urls are created.
    """
    now = datetime.strptime(
        datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "%d/%m/%Y, %H:%M:%S"
    )
    try:
        product = Product.objects.get(discovery_url=discovery_url)
        if str(product_name) != str(product.product_name):
            product.product_name = product_name
            product.last_discovery = now
            product.save()
            logging.info(f"Found Product, updating name: {product.product_name}")
        else:
            product.last_discovery = now
            product.save()
            logging.info(f"Found Product: {product.product_name}")
    except Product.DoesNotExist:
        product = Product.objects.create(
            discovery_url=discovery_url,
            product_name=product_name,
            last_discovery=now,
        )
        logging.info(f"!! CREATED New Product: {product.product_name}")
    return product
