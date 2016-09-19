from django.core.urlresolvers import reverse
from django.db import models

from django.conf import settings
from django.utils.timezone import now

from categories.mixins import CategoryMixin
from categories.models import Category
from cmskit.models import Named, ContentContainer, Publishable
from cmskit.models import TimeStamped
from cmskit.models.content_container import OptionalContentContainer
from cmskit.models.publishable import CONTENT_STATUS_PUBLISHED
from fkchooser.fields import PopupForeignKey
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


class VoterGuide(Named, OptionalContentContainer, TimeStamped):

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

    alternate_url = models.CharField(
        help_text="i.e. /elections/.  If provided, "
                  "a LIVE Voter Guide will launch this instead.",
        max_length=255,
        blank=True,
        default="/elections/"
    )

    image = models.ForeignKey(
        MediaItem,
        verbose_name="Headline image",
        null=True,
        blank=True,
        related_name="voterguides_with_image")

    def get_absolute_url(self):
        if self.alternate_url:
            return self.alternate_url
        else:
            return super(VoterGuide, self).get_absolute_url()

    def published_propositions(self, user, category=None):

        if user and user.is_staff:
            qs = self.related_propositions.all()
        else:
            qs = self.related_propositions.filter(
                status=CONTENT_STATUS_PUBLISHED)
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


#  Todo:  Move this to Article, and make it Generic
class PropRelatedArticle(models.Model):

    proposition = PopupForeignKey(
        "pages.Proposition", related_name='prop_related')
    related_article = PopupForeignKey(
        "pages.Article", related_name='related_articles')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = "Related Article"
        verbose_name_plural = "Related Articles"
        ordering = ('order', )


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

    embedded_content_title = models.CharField(
        verbose_name="title",
        max_length=50,
        default="Here's How I See It",
        blank=True)
    embedded_content_content = models.TextField(
        verbose_name="embedded content",
        default="",
        blank=True)

    video_section_title = models.CharField(
        verbose_name="title",
        max_length=50,
        default="Show me the money",
        blank=True)
    video_section_embedded_content = models.TextField(
        verbose_name="embedded video content",
        default="",
        blank=True)

    more_information = models.TextField(
        "More information", blank=True, null=True)

    supporters = models.ManyToManyField(
        PoliticalEntity,
        blank=True,
        related_name='props_with_supporter')
    opponents = models.ManyToManyField(
        PoliticalEntity,
        blank=True,
        related_name='props_with_opponents')

    related_articles = models.ManyToManyField(
        "self",
        verbose_name="Related Articles",
        through=PropRelatedArticle,
        related_name='contained_in_related',
        symmetrical=False,
        blank=True)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = "Proposition"
        verbose_name_plural = "Propositions"
        ordering = ('order', )

    def _get_ordered_related_articles(self, published_only):
        """Get headlines in order of RelatedHeadlineArticle.order"""

        qs = PropRelatedArticle.objects.filter(
            proposition=self).select_related('related_article')

        # Todo:  Dry this out, this is duplicated in Publishable.
        if published_only:
            qs.filter(
                Q(proposition__publish_date__lte=now()) |
                Q(proposition__publish_date__isnull=True),
                Q(proposition__status=CONTENT_STATUS_PUBLISHED)).order_by(
                '-publish_date')

        return [prop.related_article for prop in qs.all()]

    def get_published_ordered_related_articles(self):
        return self._get_ordered_related_articles(published_only=True)

    def get_ordered_related_articles(self):
        return self._get_ordered_related_articles(published_only=False)

    def __str__(self):
        return self.title
