from django.db import models


class Website(models.Model):
    """Base class for Website object."""

    domain = models.CharField(max_length=200, unique=True)
    main_url = models.CharField(max_length=200, unique=True)
    module_name = models.CharField(max_length=100)
    scraper_class = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.domain
