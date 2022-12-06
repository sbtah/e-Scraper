from django.db import models
from projects.models.websites import Website


class WebPage(models.Model):
    """
    Base abstract class for all other types of Pages on site.
    """

    # WebPages are instanciated by discovery url.
    discovery_url = models.CharField(max_length=255, unique=True)
    # When Webpage is requested by it's discovery_url current_url is set.
    # Used because WebPages can be redirected to new URL.
    current_url = models.CharField(max_length=255, blank=True)
    # If request suceeds WebPage is set to is_active to True or to False if fails.
    is_active = models.BooleanField(default=False)

    seo_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.CharField(max_length=255, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    parrent_website = models.ForeignKey(Website, on_delete=models.CASCADE)

    class Meta:
        abstract = True
