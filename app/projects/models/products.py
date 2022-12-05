from django.db import models
from projects.models.webpages import WebPage
from django.contrib.postgres.fields import ArrayField


class ProductPage(WebPage):
    """Class for ProductPage object where Product data is located."""

    is_active = models.BooleanField(default=True)
    parrent_categories_pages = ArrayField(
        models.IntegerField(null=True, blank=True),
        blank=True,
        null=True,
    )
    last_discovery = models.DateTimeField(blank=True, null=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.discovery_url}"


class ProductData(models.Model):
    """
    Class for Product object. Product data is always related to ProductPage.
    ProductData will be scraped daily, so ProductPage will contain different
        ProductData for each day.
    """

    # ProductData is stored for each day.
    date_of_scrape = models.DateTimeField(auto_now_add=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField(blank=True)
    product_traits = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    product_price_for_unit = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    product_unit_type = models.CharField(max_length=50, blank=True)
    product_brand = models.CharField(max_length=255, blank=True)
    product_web_id = models.CharField(max_length=255, blank=True)
    product_sku = models.CharField(max_length=255, blank=True)
    product_ean = models.CharField(max_length=13, blank=True)
    product_is_in_promo = models.BooleanField(default=False)
    product_promo_type = models.CharField(max_length=255, blank=True)
    product_warranty_time = models.CharField(max_length=100, blank=True)
    product_availability = models.BooleanField(default=False)
    product_current_stock = models.CharField(max_length=255, blank=True)
    # Products are always related to ProductPage.
    product_parrent_page = models.ForeignKey(
        ProductPage,
        on_delete=models.CASCADE,
    )
    # Sometimes Product can have a different variants.
    parrent_product = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.product_name}"


class ProductDataExtraField(models.Model):
    """
    Base abstract class for ProductExtraField.
    Used to extend Product objects with extra data.
    """

    name = models.CharField(max_length=255, blank=True)
    value = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    parrent_product = models.ForeignKey(ProductData, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ProductExtraField"
