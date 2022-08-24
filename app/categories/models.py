from django.db import models


class Category(models.Model):
    """Class for category object."""

    current_url = models.CharField(max_length=255, unique=True)
    category_name = models.CharField(max_length=255)

    is_active = models.BooleanField()
    category_description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.CharField(max_length=255, blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    parrent_category = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"
