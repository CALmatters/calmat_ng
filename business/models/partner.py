import random

from datetime import date, timedelta
from django.utils.translation import ugettext_lazy as _
from django.db import models
from versatileimagefield.fields import VersatileImageField

from business.models.partner_owner import PartnerOwner
from categories.models import Category
from media_manager.models import MediaItem
from sites.models import Named, TimeStamped

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

    featured = models.BooleanField(default=False)

    image = models.ForeignKey(
        MediaItem,
        null=True,
        blank=True,
        related_name="partner_with_image")

    image_large = models.ForeignKey(
        MediaItem,
        null=True,
        blank=True,
        related_name="partner_with_large_image")

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

    @staticmethod
    def partners():
        """Randomly choose 3 partners, return as tuple.

        1.  Chosen from featured=True partners
        2.  Chsoen from partners that are part of a radio distribution
        3.  Chosen from parnets with most number of distributions in
        last 30 days

        all 3 partners distinct.
        """

        featured_partner = Partner.objects.filter(
            featured=True).order_by('?')[0]

        from business.models.partner_article import PartnerArticle

        radio_partner = PartnerArticle.objects.filter(
            radio_broadcast=True).exclude(
            partner=featured_partner).select_related().order_by('?')[0].partner

        recent_partner = PartnerArticle.objects.filter(
            date_published__gt=date.today()-timedelta(days=30)
        ).exclude(
            partner=featured_partner).exclude(
            partner=radio_partner).order_by('?')[0].partner

        return featured_partner, radio_partner, recent_partner

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return "article_list_partner", (), {"partner": self.slug}

    def __str__(self):
        return u"{}".format(self.title)

