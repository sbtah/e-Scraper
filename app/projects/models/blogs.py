from django.db import models
from projects.models.webpages import WebPage
from django.contrib.postgres.fields import ArrayField


class BlogPage(WebPage):
    """Class for BlogPage object where all BlogArticlePages are located."""

    is_active = models.BooleanField(default=True)
    main_title = models.CharField(max_length=100, blank=True)
    main_description = models.TextField(blank=True)
    last_discovery = models.DateTimeField(blank=True, null=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.discovery_url
