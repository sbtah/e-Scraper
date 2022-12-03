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

    # I use single object for all Categories.
    # To differ root Category from childs I will use nesting levels.
    # Where root Category is 1.
    class NestLevel(models.IntegerChoices):
        first = 1
        second = 2
        third = 3
        fourth = 4
        fifth = 5
        sixth = 6

    category_nesting_level = models.IntegerField(
        choices=NestLevel.choices,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    category_description = models.TextField(blank=True)
    # Some Categories can be childs of other Categories.
    parrent_category = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    last_discovery = models.DateTimeField(blank=True, null=True)
    last_scrape = models.DateTimeField(blank=True, null=True)
    related_categories_last_discovery = models.DateTimeField(blank=True, null=True)
    related_products_last_discovery = models.DateTimeField(blank=True, null=True)
    # Same ProductPage can be in many different CategoryPages.
    products = models.ManyToManyField(ProductPage, blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "CategoryPages"
