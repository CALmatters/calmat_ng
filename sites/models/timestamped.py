from django.db import models


class TimeStamped(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)
