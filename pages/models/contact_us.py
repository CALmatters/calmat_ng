from django.db import models

from cmskit.models import TimeStamped


class ContactUs(TimeStamped):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    #  Todo:  should be rows=10 cols=40
    message = models.TextField(max_length=100)

    class Meta:
        verbose_name = "Contact Us Record"
        verbose_name_plural = "Contact Us Records"
        ordering = ('created', )
