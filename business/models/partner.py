import random

from datetime import date, timedelta
from django.utils.translation import ugettext_lazy as _
from django.db import models
# from versatileimagefield.fields import VersatileImageField

from business.models.partner_owner import PartnerOwner
from categories.models import Category
from media_manager.models import MediaItem
from sites.models import Named, TimeStamped

PARTNER_TYPES = (
    ('distribution', 'Distribution'),
    ('data', 'Data'),
)

PARTNER_TYPES_FOR_MAP = (
    ('standard', 'Standard'),
    ('radio', 'Radio'),
    ('digital', 'Digital'),
    ('national', 'National'),
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

    # featured_image = VersatileImageField(
    #     verbose_name=_("Featured Image"),
    #     upload_to="partners/",
    #     null=True,
    #     blank=True)

    # featured_image_large = VersatileImageField(
    #     verbose_name=_("Featured Image - Large"),
    #     upload_to="partners/",
    #     null=True,
    #     blank=True)

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

    # Mapbox related
    # --------------------------------------------------------------------------

    show_on_map = models.BooleanField(
        default=False,
        verbose_name=_('Include in Map'),
        help_text='Check to include on map and side list')

    map_partner_type = models.CharField(
        max_length=80,
        choices=PARTNER_TYPES_FOR_MAP,
        verbose_name=_('Map Partner Type'),
        default='standard',
        help_text='Digital and National partners \
                   DO NOT show on the map, but are listed on the sidebar')

    latitude = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=8,
        verbose_name=_('Latitude Decimal'),
        help_text="""MUST be decimal format not degrees, i.e. 34.05197222 \
                     not 34°03'07.1"N""")

    longitude = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=8,
        verbose_name=_('Longitude Decimal'),
        help_text="""MUST be decimal format not degrees, i.e. -118.2457222 \
                     not 118°14'44.6"W<br>
                     NOTE: North American logitude ending in "W" should be \
                     a negative value!""")

    short_description = models.TextField(
        blank=True,
        verbose_name=_('Map Description Text'),
        help_text='Short description that shows in the map tooltip on hover')

    # map_thumbnail = FileField(
    #     verbose_name=_("Map Thumbnail"),
    #     upload_to=upload_to(
    #         "blog.BlogPartner.map_thumbnail", "partners"),
    #     format="Image",
    #     max_length=255,
    #     null=True,
    #     blank=True)

    map_thumbnail = models.ForeignKey(
        MediaItem,
        null=True,
        blank=True,
        related_name="partner_map_tooltip_thumbnail")

    def get_geojson_dict(self):
        """
        Return a dict in GeoJSON Feature format suitable to convert to GeoJSON
        for use with Mapbox.
        """
        geojson_dict = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    self.longitude, # e.g. -118.2457222
                    self.latitude   # e.g. 34.05197222
                ]
            },
            "properties": {
                "title": self.title,    # e.g. "LA Times"
                "slug": self.slug,      # e.g. "la_times",
                "description": self.short_description,
                "url": self.get_absolute_url(),
                "partner_type": self.map_partner_type,
                "icon": {
                    "iconSize": [12, 12],
                    "className": "partner-marker-{0}".format(self.map_partner_type),
                    # "className": 'boom',
                }
            }
        }
        return geojson_dict

    def _in_california(self):
        """
        See if a partner is within California by latitude/longitude.
        """
        ca_lat = { # Approximate CA latitude range
            'min': 32.0,
            'max': 44.0,
        }
        ca_lon = { # Approximate CA longitude range
            'min': -125.0,
            'max': -114.0,
        }

        if ca_lat['min'] <= self.latitude <= ca_lat['max'] and \
           ca_lon['min'] <= self.longitude <= ca_lon['max']:
            return True
        else:
            return False
    in_california = property(_in_california)

    def partner_owner(self):
        """Lookup for admin display

        Used by Publish DB Admin, and Partner Admin to show related owner
        """
        if self.owner:
            return self.owner.title
        else:
            return ""

    @staticmethod
    def _partners(limit_to_article=None):
        """Randomly choose 3 partners, return as tuple.

        1.  Chosen from featured=True partners
        2.  Chsoen from partners that are part of a radio distribution
        3.  Chosen from parnets with most number of distributions in
        last 30 days

        all 3 partners distinct.
        """

        from business.models.partner_article import PartnerArticle

        #  First get featured partner, either over all, or related to article
        #  and, collect the pool of remaining partners
        if limit_to_article is None:
            featured_partner = Partner.objects.filter(
                featured=True).order_by('?')[0]
            partner_article_pool_qs = PartnerArticle.objects.all()
        else:
            featured_partner = limit_to_article.partners.all().order_by(
                '?')[0]
            partner_article_pool_qs = PartnerArticle.objects.filter(
                article=limit_to_article)

        try:
            radio_partner = partner_article_pool_qs.filter(
                radio_broadcast=True).exclude(
                partner=featured_partner
            ).select_related().order_by('?')[0].partner
        except IndexError:
            try:
                radio_partner = next(iter(partner_article_pool_qs)).partner
            except StopIteration:
                radio_partner = None

        try:
            recent_partner = partner_article_pool_qs.filter(
                date_published__gt=date.today()-timedelta(days=30)
            ).exclude(
                partner=featured_partner).exclude(
                partner=radio_partner).order_by('?')[0].partner
        except IndexError:
            try:
                recent_partner = next(iter(partner_article_pool_qs)).partner
            except StopIteration:
                recent_partner = None

        chosen_partners = [
            p for p in (featured_partner, radio_partner, recent_partner) if p]
        other_partners = partner_article_pool_qs.exclude(
            partner__in=chosen_partners)

        return_dict = dict(
            chosen_partners=chosen_partners,
            other_partners=other_partners,
            other_partners_len=len(other_partners))

        print(featured_partner, radio_partner, recent_partner)
        print(return_dict)

        return return_dict

    @staticmethod
    def partners():
        return Partner._partners()

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return "article_list_partner", (), {"partner": self.slug}

    def __str__(self):
        return u"{}".format(self.title)

