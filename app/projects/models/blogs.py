from django.db import models
from projects.models.webpages import WebPage


class BlogPage(WebPage):
    """Class for BlogPage object where all BlogArticlePages are located."""

    main_title = models.CharField(max_length=100, blank=True)
    main_description = models.TextField(blank=True)

    def __str__(self):
        return self.discovery_url
