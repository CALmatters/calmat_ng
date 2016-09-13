from django.db import models

from django.conf import settings
from django.utils.timezone import now

from categories.mixins import CategoryMixin
from categories.models import Category
from cmskit.models import Named, ContentContainer, Publishable
from cmskit.models import TimeStamped
from cmskit.models.publishable import CONTENT_STATUS_PUBLISHED
from media_manager.models import MediaItem


class VoterGuideManager(models.Manager):

    def in_go_live_order(self):
        return self.filter(can_go_live=True).order_by('-go_live_on_date')

    def get_live_object(self):

        n = now()

        objs = self.filter(
            can_go_live=True,
            go_live_on_date__isnull=False,
            go_live_on_date__lt=n).order_by('-go_live_on_date')

        try:
            return objs[0]
        except IndexError:
            return None


class VoterGuide(Named, TimeStamped):

    url_name = "voter_guide"

    objects = VoterGuideManager()

    category_in_menu = models.BooleanField(
        verbose_name="Category in menus",
        help_text=("If checked, the main menu will show categories.  "
                   "If not checked the main menu will show propositions."),
        default=True)

    can_go_live = models.BooleanField(default=False)
    go_live_on_date = models.DateTimeField(
        help_text="Times are in {}".format(settings.TIME_ZONE),
        unique=True,
        null=True,
        blank=True)

    def published_propositions(self, category=None):

        qs = self.related_propositions.filter(status=CONTENT_STATUS_PUBLISHED)
        if category:
            qs = qs.filter(categories=category)

        return qs

    def published_propositions_categories(self):
        cats = set(
            [cat for prop in self.related_propositions.filter(
                    status=CONTENT_STATUS_PUBLISHED)
                for cat in prop.categories.all()])

        return cats

    def has_props(self):
        return self.related_propositions.filter(
            status=CONTENT_STATUS_PUBLISHED).exists()


class PoliticalEntity(Named):

    url_name = "political_entity"

    image = models.ForeignKey(
        MediaItem,
        verbose_name="Icon",
        null=True,
        blank=True,
        related_name="entities_with_image")


class Proposition(Named, ContentContainer, Publishable, TimeStamped,
                  CategoryMixin):

    DEFAULT_IMAGE = "theme/frontend/img/featured-image-default.jpg"

    url_name = "proposition_detail"


    voter_guide = models.ForeignKey(
        VoterGuide, related_name='related_propositions')

    categories = models.ManyToManyField(
        Category,
        verbose_name="Categories",
        blank=True,
        related_name="props_in_category")

    image = models.ForeignKey(
        MediaItem,
        verbose_name="Icon Image",
        null=True,
        blank=True,
        related_name="props_with_image")

    more_information = models.TextField(
        "More information", blank=True, null=True)

    supporters = models.ManyToManyField(
        PoliticalEntity, related_name='props_with_supporter')
    opponents = models.ManyToManyField(
        PoliticalEntity, related_name='props_with_opponents')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = "Proposition"
        verbose_name_plural = "Propositions"
        ordering = ('order', )

    def __str__(self):
        return self.title
