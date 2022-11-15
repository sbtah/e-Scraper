from django.db import models


class Store(models.Model):
    """Class for Store object."""

    domain_name = models.CharField(max_length=100, unique=True)
    root_url = models.CharField(max_length=255, unique=True)
    home_page_url = models.CharField(max_length=255, blank=True)
    about_page_url = models.CharField(max_length=255, blank=True)
    blog_root_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.domain_name