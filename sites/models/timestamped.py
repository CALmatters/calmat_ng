from django.db import models
from django.utils.timezone import now


class TimeStamped(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
