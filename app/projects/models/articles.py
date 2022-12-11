from django.db import models
from projects.models.webpages import WebPage
from projects.models.blogs import BlogPage
from django.contrib.postgres.fields import ArrayField


class BlogArticlePage(WebPage):
    """Class for BlogArticlePage object."""

    blog_title = models.CharField(max_length=255, unique=True)
    main_description = models.TextField(blank=True)
    blog_author = models.CharField(max_length=255, blank=True)
    blog_tags = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    date_published = models.DateTimeField(blank=True, null=True)
    parrent_blog_page = models.ForeignKey(BlogPage, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog_title
