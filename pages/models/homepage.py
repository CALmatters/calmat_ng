import logging

import json, decimal # to encode python decimal into json
import operator # reduce Q statements
from copy import copy
from functools import reduce

from django.utils.timezone import now
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Q

from business.models import Partner, Person
from fkchooser.fields import PopupForeignKey
from media_manager.models import MediaItem
from pages.models import Article, Atom
from cmskit.models import Named, TimeStamped

HOME_ATOM_LAYOUT_CHOICES = (
    ('image', 'Image Layout'),
    ('embedded', 'Embedded HTML')
)

logger = logging.getLogger(__name__)

class RelatedAtom(models.Model):

    homepage = models.ForeignKey(
        "pages.HomePage", related_name='related_atom_homepages')
    atom = PopupForeignKey(
        "pages.Atom", related_name='related_atom_atoms')

    atom_layout = models.CharField(
        max_length=20,
        choices=HOME_ATOM_LAYOUT_CHOICES,
        
        default='image')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return u''

    class Meta:
        verbose_name = _("Related Atom")
        verbose_name_plural = _("Related Atoms")
        ordering = ('order', )


class RelatedHeadlineArticle(models.Model):

    homepage = models.ForeignKey(
        "pages.HomePage", related_name='related_headline_articles_as_homepage')
    article = PopupForeignKey(
        "pages.Article", related_name='related_headline_articles_as_homepage')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return u''

    class Meta:
        verbose_name = _("Related Headline Article")
        verbose_name_plural = _("Related Headline Articles "
                                "- first one is large")
        ordering = ('order', )


class HomePageManager(models.Manager):

    def in_go_live_order(self):
        return self.filter(can_go_live=True).order_by('-go_live_on_date')

    def get_live_object(self):

        n = now()

        objs = self.filter(
            can_go_live=True,
            go_live_on_date__isnull=False,
            go_live_on_date__lt=n).order_by('-go_live_on_date')

        return objs[0]


class HomePage(Named, TimeStamped):
    """The HomePage is a special page with it's one design.

    The HomePage may change dailing.  Only one HomePage at a time can
    be published.  Any number can be draft (not published).
    """

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")
        ordering = ("-go_live_on_date", )

    objects = HomePageManager()

    can_go_live = models.BooleanField(default=False)
    go_live_on_date = models.DateTimeField(
        help_text="Times are in {}".format(settings.TIME_ZONE),
        unique=True,
        null=True,
        blank=True)

    masthead_copy = models.CharField(
        max_length=125,
        default=settings.MASTHEAD_DEFAULT,
        help_text="Text displayed in top black bar for the homepage."
    )

    # IN THE WORKS
    # Todo:  Validate that if a url or display is filled in, other needs to be
    works_display_one = models.CharField(
        verbose_name="Works 1 Label",
        max_length=25,
        help_text="25 characters max",
        blank=True,
        default='')
    works_url_one = models.CharField(
        verbose_name="Works 1 URL",
        max_length=500,
        help_text="A valid http:// or https:// link",
        blank=True,
        default='')

    works_display_two = models.CharField(
        verbose_name="Works 2 Label",
        max_length=25,
        help_text="25 characters max",
        blank=True,
        default='')
    works_url_two = models.CharField(
        verbose_name="Works 2 URL",
        max_length=500,
        help_text="A valid http:// or https:// link",
        blank=True,
        default='')

    works_display_three = models.CharField(
        verbose_name="Works 3 Label",
        max_length=25,
        help_text="25 characters max",
        blank=True,
        default='')
    works_url_three = models.CharField(
        verbose_name="Works 3 URL",
        max_length=500,
        help_text="A valid http:// or https:// link",
        blank=True,
        default='')

    works_display_four = models.CharField(
        verbose_name="Works 4 Label",
        max_length=25,
        help_text="25 characters max",
        blank=True,
        default='')
    works_url_four = models.CharField(
        verbose_name="Works 4 URL",
        max_length=500,
        help_text="A valid http:// or https:// link",
        blank=True,
        default='')

    works_display_five = models.CharField(
        verbose_name="Works 5 Label",
        max_length=25,
        help_text="25 characters max",
        blank=True,
        default='')
    works_url_five = models.CharField(
        verbose_name="Works 5 URL",
        max_length=500,
        help_text="A valid http:// or https:// link",
        blank=True,
        default='')

    primary_article = PopupForeignKey(
        Article,
        help_text="Article displayed front and center, largest",
        verbose_name='Primary Article',
        related_name='primary_on_homepages',
    )

    secondary_article_left = PopupForeignKey(
        Article,
        help_text="Article displayed below primary article to the left",
        verbose_name='Left Secondary Article',
        related_name='secondary_left_on_homepages',
    )

    secondary_article_right = PopupForeignKey(
        Article,
        help_text="Article displayed below primary article to the right",
        verbose_name='Right Secondary Article',
        related_name='secondary_right_on_homepages',
    )

    the_basics_one = PopupForeignKey(
        Article,
        url_filter='custom_post_type__exact=basics',
        help_text="First Article in the The Basics",
        verbose_name='Top Article in The Basics',
        related_name='basics_one_on_homepages',
    )

    the_basics_two = PopupForeignKey(
        Article,
        url_filter='custom_post_type__exact=basics',
        help_text="Second Article in the The Basics",
        verbose_name='Second Article in The Basics',
        related_name='basics_two_on_homepages',
    )

    the_basics_three = PopupForeignKey(
        Article,
        url_filter='custom_post_type__exact=basics',
        help_text="Third Article in the The Basics",
        verbose_name='Third Article in The Basics',
        related_name='basics_three_on_homepages',
    )

    the_basics_four = PopupForeignKey(
        Article,
        url_filter='custom_post_type__exact=basics',
        help_text="Four Article in the The Basics",
        verbose_name='Bottom Article in The Basics',
        related_name='basics_four_on_homepages',
    )

    featured_2 = PopupForeignKey(
        Article,
        verbose_name='Second Feature',
        blank=True,
        null=True,
        related_name='home_featured_2')

    headlines = models.ManyToManyField(
        Article,
        blank=True,
        verbose_name='More Headlines',
        through='RelatedHeadlineArticle',
        related_name='home_more_headlines')

    atoms = models.ManyToManyField(
        Atom,
        verbose_name='Related Atoms',
        blank=True,
        related_name='homepages_with_atom',
        through='RelatedAtom')

    politics_author = models.ForeignKey(Person, blank=True, null=True)
    #  Limitation with popup image chooser is that image must be named 'image'
    #  this restriction is found in popup_v1.js.
    # Todo:  allow for more than one image per page.
    image = models.ForeignKey(
        MediaItem,
        verbose_name="Politics Image",
        null=True,
        blank=True,
        related_name="homepage_with_politics_image",
        help_text="Show this image instead of the author's image.")

    politics_quote = models.TextField(max_length=500, default='', blank=True)
    politics_quote_attribution = models.CharField(
        max_length=135, default='', blank=True)

    template_filename = models.CharField(
        max_length=255,
        default='home.html',
        help_text="Can provide an alternative home page template to use.  "
                  "If you aren't sure what to do, then do not change this "
                  "value.")

    def recent_politics_articles(self):
        """Return most recent 3 published politics articles"""

        return Article.objects.published().filter(news_analysis=True)[:3]

    def politics_image(self):
        return self.politics_alternate_image or (
            self.politics_author and self.politics_author.image)

    def recent_articles(self):
        """Return most recent 3 published politics articles"""

        return Article.objects.published().exclude(
            news_analysis=True).exclude(
            custom_post_type='readerreactions').exclude(
            custom_post_type='press').exclude(
            custom_post_type='external').exclude(
            custom_post_type='basics')[:3]

    def clone(self):
        _clone = copy(self)
        _clone.pk = None
        _clone.title = "{} copy".format(self.title)
        _clone.can_go_live = False
        _clone.go_live_on_date = None
        _clone.created = None
        _clone.updated = None
        _clone.slug = None

        _clone.save()

        rel_models = [RelatedHeadlineArticle, RelatedAtom]
        for rel_model in rel_models:
            for rel in rel_model.objects.filter(homepage=self):
                rel = copy(rel)
                rel.homepage = _clone
                rel.save()

        return _clone
    clone.short_description = "Duplicate"

    def get_absolute_url(self):
        return "/"


    def has_in_the_works(self):
        return any(bool(d['label'] and d['url'])
                   for d in self.yield_in_the_works_titles())

    def yield_in_the_works_titles(self):
        """Iterator for the 0-5 in the works label/url pairs

        Todo:  this isn't DRY or scalable.  Watch it for improvements.
        """

        for idx in ['one', 'two', 'three', 'four', 'five']:
            label_attr = 'works_display_{}'.format(idx)
            url_attr = 'works_url_{}'.format(idx)
            label = getattr(self, label_attr, None)
            url = getattr(self, url_attr, None)
            if label and url:
                yield dict(label=label, url=url)

    def yield_the_basics(self):
        """Iterator for the 4 'the basics' articles"""

        for idx in ['one', 'two', 'three', 'four']:
            attr = 'the_basics_{}'.format(idx)
            article = getattr(self, attr, None)
            yield article

    def yield_ordered_headline_articles(self):
        """Get headlines in order of RelatedHeadlineArticle.order"""

        return [a.article for a in RelatedHeadlineArticle.objects.filter(
            homepage=self).select_related('article')]

    @classmethod
    def recent_projects(clazz):
        """Iterate out the top five most recent projects"""

        from pages.models import Project

        projects = getattr(clazz, 'projects', [])

        if not projects:
            for p in Project.objects.all().order_by('-publish_date'):
                projects.append(p)
            clazz.projects = projects
            logger.debug("cache miss on projects")

        return projects


    @property
    def partners(self):
        return Partner.partners()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.projects = None

        super(HomePage, self).save(
            force_insert, force_update, using,update_fields)

#-------------------------------------------------------------------------------
#   :: Home Map / Mapbox
#-------------------------------------------------------------------------------

class HomePartnerMap:

    def __init__(self):
        """
        Initialize data part of the Mapbox map:
            1. Get all the partners for the map
            2. Build the geojson Python dict object
            3. Convert geojson Python dict object to JSON string
        """

        ca_lat = { # Approximate CA latitude range
            'min': 32.0,
            'max': 44.0,
        }
        ca_lon = { # Approximate CA longitude range
            'min': -125.0,
            'max': -114.0,
        }

        # Get all mapable partners
        self.show_partners = Partner.objects.filter(show_on_map=True)

        # Partners with markers on the map: 'standard' or 'radio' AND within california
        self.map_partners = self.show_partners.filter(
                map_partner_type__in=['standard', 'radio'],
                latitude__range=(ca_lat['min'], ca_lat['max']),
                longitude__range=(ca_lon['min'], ca_lon['max']))

        # Sidebar list of standard partners, if in CA
        self.standard_partner_list = self.show_partners.filter(
                map_partner_type='standard',
                latitude__range=(ca_lat['min'], ca_lat['max']),
                longitude__range=(ca_lon['min'], ca_lon['max']))

        # Sidebar list of radio partners, anywhere
        self.radio_partner_list = self.show_partners.filter(
                map_partner_type='radio')

        # Sidebar list of digital/national or standard outside of CA, exclude radio
        Q_map_partner_type = Q(map_partner_type__in=['digital', 'national'])
        Q_list = [
            # 'digital' or 'national'
            Q(map_partner_type__in=['digital', 'national']),
            # outside of California
            Q(latitude__lt=ca_lat['min']),
            Q(latitude__gt=ca_lat['max']),
            Q(longitude__lt=ca_lon['min']),
            Q(longitude__gt=ca_lon['max']),
        ]
        self.digital_national_partner_list = self.show_partners.filter(
            reduce(operator.or_, Q_list)
        ).exclude(map_partner_type='radio')

        self.geojson_dict = {
            "type": "FeatureCollection",
            "features": []
        }

        # Append each partner to geojson features list for markers
        self._fill_features_list()

        # Make GeoJSON string to serve to Mapbox
        self.json = self._convert_to_json()

    def _fill_features_list(self):
        """
        Get geojson_dict for each BlogPartner and append to 'features' list
        in HomePartnerMap.geojson_dict.

        Filter out digital/national partners.
        """

        for partner in self.map_partners:
            feature_dict = partner.get_geojson_dict()
            self.geojson_dict['features'].append(feature_dict)

    def _convert_to_json(self):
        """
        Uses DecimalEncoder (class below) to encode latitude/longitude
        DecimalField values from BlogPartner for JSON output.
        """
        geojson = json.dumps(self.geojson_dict, cls=DecimalEncoder)
        return geojson


#-------------------------------------------------------------------------------
#   :: Utility
#-------------------------------------------------------------------------------

class DecimalEncoder(json.JSONEncoder):
    """
    Custom encoder for Python decimals.
    Used for HomePartnerMap to encode latitude/logitude DecimalFields values
    to in json.dump().
    """
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
