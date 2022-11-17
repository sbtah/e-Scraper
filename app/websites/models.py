from django.db import models


class Website(models.Model):
    """Base class for Website object."""

    domain = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.domain
