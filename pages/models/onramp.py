from django.db import models

from sites.models import ContentContainer, Named


class OnRamp(Named, ContentContainer):

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
        verbose_name = "OnRamp"
        verbose_name_plural = "OnRamps"
        ordering = ("title",)
