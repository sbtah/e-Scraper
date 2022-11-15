from django.db import models


class BasePage(models.Model):
    """
    Meta class for base Page object.
    """

    discovery_url = models.CharField(max_length=255, unique=True)
    current_url = models.CharField(max_length=255, blank=True)
    meta_author = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.CharField(max_length=255, blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True