from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# TODO:
# Design an algorythmic way of generating ID numbers
# For example root categories will have a single number id (ie: 1, 2, 12...)
# While childs will have a numbers with '0' preceding
# 1st lvl childs: (01, 02, 012)
# 2nd lvl childs: (001, 002, 003, 0012)


class Category(models.Model):
    """Class for category object."""

    current_url = models.CharField(max_length=255, unique=True)
    category_name = models.CharField(max_length=255)

    # If this is True, then this category does not have any parrents.
    is_root = models.BooleanField(default=True)
    is_active = models.BooleanField(blank=True, null=True)
    category_description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.CharField(max_length=255, blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    # Some Categories can be childs of other Categories.
    parrent_category = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        """Custom save method that changes is_root to False if Category was added as a child of another."""
        super().save(*args, **kwargs)
        if self.parrent_category:
            self.is_root = False

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"
