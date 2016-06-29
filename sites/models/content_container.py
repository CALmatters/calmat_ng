from django.db import models


class ContentContainer(models.Model):

    class Meta:
        abstract = True

    content = models.TextField("Content")


class OptionalContentContainer(models.Model):

    class Meta:
        abstract = True

    content = models.TextField("Content", blank=True, null=True)
