from django.db import models
from projects.models.webpages import WebPage


class ContactPage(WebPage):
    """Class for ContactPage object."""

    is_active = models.BooleanField(default=True)
    company_name = models.CharField(max_length=255, unique=True)
    company_address = models.TextField(blank=True)
    company_phone = models.CharField(max_length=255, blank=True)
    company_email_address = models.EmailField(blank=True)
    last_discovery = models.DateTimeField(blank=True, null=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.company_name
