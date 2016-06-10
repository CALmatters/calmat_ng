from django.utils.translation import ugettext_lazy as _
from django.db import models


class ContentContainer(models.Model):

    class Meta:
        abstract = True

    content = models.TextField(_("Content"))

