from django.db import models
from projects.models.webpages import WebPage
from django.contrib.postgres.fields import ArrayField


class BlogPage(WebPage):
    """Class for BlogPage object."""

    blog_title = models.CharField(max_length=255, unique=True)
    blog_author = models.CharField(max_length=255)
    blog_tags = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    date_published = models.DateTimeField(blank=True, null=True)
    last_discovery = models.DateTimeField(blank=True, null=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.blog_title
