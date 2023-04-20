from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from projects.models.webpages import WebPage
from projects.models.products import ProductPage

# TODO:
# Design an algorythmic way of generating ID numbers
# For example root categories will have a single number id (ie: 1, 2, 12...)
# While childs will have a numbers with '0' preceding
# 1st lvl childs: (01, 02, 012)
# 2nd lvl childs: (001, 002, 003, 0012)


class CategoryPage(WebPage):
    """Class for Category Page object."""

    category_name = models.CharField(max_length=255)
    category_description = models.TextField(blank=True)

    have_products = models.BooleanField(default=False)
    have_categories = models.BooleanField(default=True)

    categories = models.ManyToManyField("self", blank=True)
    products = models.ManyToManyField(ProductPage, blank=True)

    related_categories_last_discovery = models.DateTimeField(blank=True, null=True)
    related_products_last_discovery = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "CategoryPages"
