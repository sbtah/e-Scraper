from django.db import models
from projects.models.webpages import WebPage


class HomePage(WebPage):
    """Class for Home Page object."""

    main_title = models.CharField(max_length=100)
    main_description = models.TextField()

    def __str__(self):
        return self.title
