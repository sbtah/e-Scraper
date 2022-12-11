from django.db import models


class Website(models.Model):
    """Base class for Website object."""

    domain = models.CharField(max_length=200, unique=True)
    is_monitored = models.BooleanField(default=False)
    # Name of file for related Scraper.
    module_name = models.CharField(max_length=100)
    # Name of class for related Scraper.
    scraper_class = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.domain
