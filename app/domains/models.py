from django.db import models


class Domain(models.Model):
    """Class for Domain object."""

    name = models.CharField(max_length=255, unique=True)
    main_url = models.CharField(max_length=255, unique=True)
