from django.utils.translation import ugettext_lazy as _
from django.db import models
from versatileimagefield.fields import VersatileImageField

from business.models.partner_owner import PartnerOwner
from categories.models import Category
from sites.models import Named, TimeStamped, ContentContainer

PARTNER_TYPES = (
    ('distribution', 'Distribution'),
    ('data', 'Data'),
)


# Todo:  Consider refactoring to a general concept:  organization
class Partner(Named, TimeStamped):

    partner_type = models.CharField(
        max_length=80, choices=PARTNER_TYPES, default='distribution')

    link_to_articles = models.BooleanField(
        default=True, help_text='Add link to article list')

    featured_image = VersatileImageField(
        verbose_name=_("Featured Image"),
        upload_to="partners/",
        null=True,
        blank=True)

    featured_image_large = VersatileImageField(
        verbose_name=_("Featured Image - Large"),
        upload_to="partners/",
        null=True,
        blank=True)

    categories = models.ManyToManyField(
        Category,
        verbose_name=_("Categories"),
        blank=True,
        related_name="partners")

    owner = models.ForeignKey(
        PartnerOwner,
        related_name="partners_by_owner",
        null=True,
        blank=True)

    def partner_owner(self):
        """Lookup for admin display

        Used by Publish DB Admin, and Partner Admin to show related owner
        """
        if self.owner:
            return self.owner.title
        else:
            return ""

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return "article_list_partner", (), {"partner": self.slug}

    def __str__(self):
        return u"{}".format(self.title)

