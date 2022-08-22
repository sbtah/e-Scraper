from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    """Class for Product object."""

    # Values that will come from discovery process.
    #  When parsing URLS/NAMES at Category page.
    current_url = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)

    product_brand = models.CharField(max_length=255, blank=True)
    product_sku = models.CharField(max_length=255, blank=True, unique=True)
    product_description = models.TextField()
    product_traits = ArrayField(models.CharField(max_length=100, blank=True))
    product_promo_type = models.CharField(max_length=255, blank=True)
    product_price_for_unit = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    product_unit_type = models.CharField(max_length=20, blank=True)
    roduct_price_for_piece = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
