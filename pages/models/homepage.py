from copy import copy

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from pages.models import Article
from sites.models import Named, Publishable, TimeStamped
from sites.models.publishable import CONTENT_STATUS_DRAFT


class HomePage(Named, Publishable, TimeStamped):
    """The HomePage is a special page with it's one design.

    The HomePage may change dailing.  Only one HomePage at a time can
    be published.  Any number can be draft (not published).
    """

    masthead_copy = models.CharField(
        max_length=125,
        default=settings.MASTHEAD_DEFAULT,
        help_text="Text displayed in top black bar for the homepage."
    )

    # IN THE WORKS
    # Todo:  Validate that if a url or display is filled in, other needs to be
    works_display_one = models.CharField(
        verbose_name="Label",
        max_length=20,
        blank=True, default='')
    works_url_one = models.CharField(
        verbose_name="URL",
        max_length=20,
        help_text="A valid http:// or https:// link",
        blank=True, default='')

    works_display_two = models.CharField(
        verbose_name="Label",
        max_length=20,
        blank=True, default='')
    works_url_two = models.CharField(
        verbose_name="URL",
        max_length=20,
        help_text="A valid http:// or https:// link",
        blank=True, default='')

    works_display_three = models.CharField(
        verbose_name="Label",
        max_length=20,
        blank=True, default='')
    works_url_three = models.CharField(
        verbose_name="URL",
        max_length=20,
        help_text="A valid http:// or https:// link",
        blank=True, default='')

    works_display_four = models.CharField(
        verbose_name="Label",
        max_length=20,
        blank=True, default='')
    works_url_four = models.CharField(
        verbose_name="URL",
        max_length=20,
        help_text="A valid http:// or https:// link",
        blank=True, default='')

    works_display_five = models.CharField(
        verbose_name="Label",
        max_length=20,
        blank=True, default='')
    works_url_five = models.CharField(
        verbose_name="URL",
        max_length=20,
        help_text="A valid http:// or https:// link",
        blank=True, default='')

    primary_article = models.ForeignKey(
        Article,
        help_text="Article displayed front and center, largest",
        verbose_name='Primary Article',
        related_name='primary_on_homepages',
    )

    secondary_article_left = models.ForeignKey(
        Article,
        help_text="Article displayed below primary article to the left",
        verbose_name='Left Secondary Article',
        related_name='secondary_left_on_homepages',
    )

    secondary_article_right = models.ForeignKey(
        Article,
        help_text="Article displayed below primary article to the right",
        verbose_name='Right Secondary Article',
        related_name='secondary_right_on_homepages',
    )

    the_basics_one = models.ForeignKey(
        Article,
        help_text="First Article in the The Basics",
        verbose_name='Top Article in The Basics',
        related_name='basics_one_on_homepages',
    )

    the_basics_two = models.ForeignKey(
        Article,
        help_text="Second Article in the The Basics",
        verbose_name='Second Article in The Basics',
        related_name='basics_two_on_homepages',
    )

    the_basics_three = models.ForeignKey(
        Article,
        help_text="Third Article in the The Basics",
        verbose_name='Third Article in The Basics',
        related_name='basics_three_on_homepages',
    )

    the_basics_four = models.ForeignKey(
        Article,
        help_text="Four Article in the The Basics",
        verbose_name='Bottom Article in The Basics',
        related_name='basics_four_on_homepages',
    )

    def clone(self):
        _clone = copy(self)
        _clone.pk = None
        _clone.title = "{} copy".format(self.title)
        _clone.status = CONTENT_STATUS_DRAFT
        _clone.created = None
        _clone.updated = None
        _clone.slug = None
        _clone.publish_date = None

        _clone.save()

        #  Todo:  Copy M2M records

        return _clone
    clone.short_description = "Duplicate"

    def get_absolute_url(self):
        return "/"

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")
        ordering = ("status", )
