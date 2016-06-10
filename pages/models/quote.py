from django.db import models

from sites.models import ContentContainer, Named


class Quote(Named, ContentContainer):
    """
    Nameds for title, brings in Description and Slug, which are not used
    ContentContainer for Content
    """

    attribution = models.CharField(
        verbose_name="Attribution",
        max_length=255,
        default='',
        blank=True)

    custom_link = models.CharField(
        verbose_name="More Link",
        max_length=1200,
        default='',
        blank=True)

    def get_absolute_url(self):
        """Required by Named, but not used."""

        name = self.__class__.__name__
        raise NotImplementedError("The model %s does not have "
                                  "get_absolute_url defined" % name)

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ("title",)
