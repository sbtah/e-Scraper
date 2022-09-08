from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    """Class for Product object."""

    # Values that will come from discovery process.
    # When parsing URLS/NAMES at Category page.
    discovery_url = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)

    # Since Products can be redirected also....
    current_url = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(blank=True, null=True)
    product_brand = models.CharField(max_length=255, blank=True)
    product_sku = models.CharField(max_length=255, blank=True)
    product_description = models.TextField(blank=True)
    # Not tracked in scraper yet.
    meta_description = models.TextField(blank=True)
    # Not tracked in scraper yet.
    canonical_url = models.CharField(max_length=255, blank=True)
    # Not tracked in scraper yet.
    seo_title = models.CharField(max_length=255, blank=True)
    product_traits = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    product_promo_type = models.CharField(max_length=255, blank=True)
    product_warranty_time = models.CharField(max_length=100, blank=True)
    product_ean = models.CharField(max_length=13, blank=True)
    parrent_categories = ArrayField(
        models.IntegerField(null=True, blank=True),
        blank=True,
        null=True,
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    last_discovery = models.DateTimeField(blank=True, null=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product_name}"


class ProductLocalData(models.Model):
    """
    Class for Product's data for local store only.
    """

    is_tracked = models.BooleanField(default=False)
    store_name = models.CharField(max_length=255, blank=True)
    product_availability = models.BooleanField(default=False)
    product_current_stock = models.CharField(max_length=255, blank=True)
    product_price_for_unit = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    product_unit_type = models.CharField(max_length=50, blank=True)
    product_price_for_piece = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    product_piece_type = models.CharField(max_length=50, blank=True)
    product_price_before_promo = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    product_availability = models.CharField(max_length=50, blank=True)
    product_current_stock = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    parrent_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.store_name}"

    class Meta:
        verbose_name_plural = "ProductLocalData"


class ProductExtraField(models.Model):
    """
    Class for product's extra field.
    Used to extend Product object with extra data,
        that I will decide to scrape in the future.
    """

    name = models.CharField(max_length=255, blank=True)
    value = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    parrent_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "ProductExtraField"
