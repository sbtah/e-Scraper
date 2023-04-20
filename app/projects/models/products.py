from django.db import models
from projects.models.webpages import WebPage
from django.contrib.postgres.fields import ArrayField


class ProductPage(WebPage):
    """Class for ProductPage object where Product data is located."""

    parrent_categories_pages = ArrayField(
        models.IntegerField(null=True, blank=True),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"ProductPage: {self.discovery_url}"


class ProductData(models.Model):
    """
    Class for ProductData object. Product data is always related to ProductPage.
    ProductData will be scraped daily, so ProductPage will contain different
        ProductData for each day.
    """

    date_of_scrape = models.DateTimeField(auto_now_add=True)

    product_name = models.CharField(max_length=255)

    product_parrent_page = models.ForeignKey(
        ProductPage,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.product_name}"


class ProductDataField(models.Model):
    """
    Class for ProductDataField object.
    Used for dynamically store data for ProducData objects.
    """

    field_name = models.CharField(max_length=255)
    field_value = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    parrent_product = models.ForeignKey(ProductData, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ProductDataFields"
