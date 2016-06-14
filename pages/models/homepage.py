from copy import copy

from django.utils.timezone import now
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from business.models import Partner, Author
from pages.models import Article
from sites.models import Named, TimeStamped


class RelatedHeadlineArticle(models.Model):

    homepage = models.ForeignKey(
        "pages.HomePage", related_name='related_headline_articles_as_homepage')
    article = models.ForeignKey(
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
        print(n, n.tzinfo)
        for o in self.all():
            print(o.title, o.go_live_on_date, o.go_live_on_date.tzinfo)

        objs = self.filter(
            can_go_live=True,
            go_live_on_date__lt=n).order_by('-go_live_on_date')

        return objs[0]


class HomePage(Named, TimeStamped):
    """The HomePage is a special page with it's one design.

    The HomePage may change dailing.  Only one HomePage at a time can
    be published.  Any number can be draft (not published).
    """

    objects = HomePageManager()

    can_go_live = models.BooleanField(default=False)
    go_live_on_date = models.DateTimeField(
        help_text="Times are in {}".format(settings.TIME_ZONE),
        unique=True)

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

    featured_2 = models.ForeignKey(
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

    politics_author = models.ForeignKey(Author, blank=True, null=True)

    politics_quote = models.TextField(max_length=500, default='', blank=True)

    def recent_politics_articles(self):
        """Return most recent 3 published politics articles"""

        return Article.objects.published().filter(news_analysis=True)[:3]

    def recent_non_politics_articles(self):
        """Return most recent 3 published politics articles"""

        return Article.objects.published().exclude(news_analysis=True)[:3]

    #  TODO:  Atoms will be m2m an displayed in a carousel
    # atom = models.ForeignKey(
    #     Atom,
    #     verbose_name='Home Atom',
    #     blank=True,
    #     null=True,
    #     related_name='home_atom',
    #     help_text='Appears below external link carousel.')
    #
    # atom_layout = models.CharField(max_length=20,
    #                                choices=HOME_ATOM_LAYOUT_CHOICES,
    #                                help_text='Home atom layout',
    #                                default='image')

    def clone(self):
        _clone = copy(self)
        _clone.pk = None
        _clone.title = "{} copy".format(self.title)
        _clone.can_go_live = False
        _clone._go_live_on_date = now()
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


    @staticmethod
    def yield_recent_projects():
        """Iterate out the top five most recent projects"""

        from pages.models import Project

        for p in Project.objects.all().order_by('-publish_date')[:5]:
            yield p


    @property
    def partners(self):
        return Partner.partners()

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")
        ordering = ("-go_live_on_date", )
