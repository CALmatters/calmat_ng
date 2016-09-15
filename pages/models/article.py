import re
from copy import copy

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from categories.mixins import CategoryMixin
from fkchooser.fields import PopupForeignKey
from media_manager.models import MediaItem
from .atom import Atom
from business.models import Partner, Person

from categories.models import Category
from cmskit.models import Named, Publishable, TimeStamped, ContentContainer
from cmskit.models.publishable import CONTENT_STATUS_DRAFT, \
    CONTENT_STATUS_PUBLISHED

CUSTOM_POST_TYPE_CHOICES = (
    ('articles', 'Articles'),
    ('expertperspectives', 'Expert Perspectives'),
    ('external', 'External Link'),
    ('press', 'Press Release'),
    ('readerreactions', 'Reader Reactions'),
    ('updates', 'Updates'),
    ('basics', 'The Basics'),
)

BLOG_POST_LAYOUT_CHOICES = (
    ('sidebar', 'Sidebar'),
    ('singlecolumn', 'Single Column'),
)

HEADLINE_LAYOUT_CHOICES = (
    ('below', 'Below Image'),
    ('below_big', 'Below Image - Big'),
    ('over', 'Over Image'),
    ('above', 'Above Image'),
)

FEATURED_IMAGE_TITLE_POSITION = (
    ('topleft', 'Top-Left'),
    ('topright', 'Top-Right'),
    ('bottomleft', 'Bottom-Left'),
    ('bottomright', 'Bottom-Right'),
)
FEATURED_IMAGE_TITLE_SHADE = (
    ('dark', 'Dark'),
    ('light', 'Light'),
)


class RelatedArticle(models.Model):

    article = PopupForeignKey(
        "pages.Article", related_name='main_post')
    related_article = PopupForeignKey(
        "pages.Article", related_name='related_post')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = _("Related Article")
        verbose_name_plural = _("Related Articles")
        ordering = ('order', )


class Article(Named, Publishable, ContentContainer, TimeStamped, CategoryMixin):

    DEFAULT_ARTICLE_IMAGE = "theme/frontend/img/featured-image-default.jpg"

    SEARCH_FIELDS = ['title', 'description', 'content']

    custom_post_type = models.CharField(
        verbose_name=_("Content Type"),
        max_length=30,
        choices=CUSTOM_POST_TYPE_CHOICES,
        default='articles')

    news_analysis = models.BooleanField(
        verbose_name=_("Politics"),
        default=False,
        help_text="Check this box if this article "
                  "should display in the POLITICS Menu")

    layout = models.CharField(
        verbose_name=_("Layout"),
        max_length=30,
        choices=BLOG_POST_LAYOUT_CHOICES,
        default='sidebar')

    social_title = models.CharField(
        verbose_name=_("Social Sharing Title"),
        help_text="Title used when submitting article to social sites.",
        max_length=200,
        default='',
        blank=True)

    # External link stuff
    custom_source = models.CharField(
        verbose_name=_("External Source"),
        max_length=255,
        default='',
        blank=True)

    custom_link = models.CharField(
        verbose_name=_("External Link"),
        max_length=1200,
        blank=True)

    # Related Objects
    atoms = models.ManyToManyField(
        Atom,
        verbose_name=_("Atoms"),
        blank=True,
        related_name="blogposts")

    related_posts = models.ManyToManyField(
        "self",
        verbose_name=_("Related Posts"),
        through=RelatedArticle,
        related_name='contained_in_related',
        symmetrical=False,
        blank=True)

    partners = models.ManyToManyField(
        Partner,
        through="business.PartnerArticle",
        verbose_name=_("Partners"),
        blank=True,
        related_name="articles_by_partner",
    )

    categories = models.ManyToManyField(
        Category,
        verbose_name="Categories",
        blank=True,
        related_name="blogposts")

    authors = models.ManyToManyField(
        Person,
        verbose_name="Person",
        blank=True,
        related_name="authors_articles",
        help_text='Choices limited to users who are staff (is_staff=True).')

    guest_author = models.CharField(
        verbose_name="Guest Author",
        max_length=100,
        default='',
        blank=True,
        help_text="*Guest Author* will be prepend regular "
                  "Authors selected above.")

    headline_layout = models.CharField(
        verbose_name=_("Headline Layout"),
        max_length=30,
        choices=HEADLINE_LAYOUT_CHOICES,
        default='below')

    image = models.ForeignKey(
        MediaItem,
        verbose_name="Featured Image",
        null=True,
        blank=True,
        related_name="article_with_image")

    featured_image_title_position = models.CharField(
        verbose_name=_("Position"),
        max_length=30,
        choices=FEATURED_IMAGE_TITLE_POSITION,
        default='topleft')

    featured_image_title_shade = models.CharField(
        verbose_name=_("Shade"),
        max_length=30,
        choices=FEATURED_IMAGE_TITLE_SHADE,
        default='dark')

    featured_image_description = models.CharField(
        verbose_name=_("Image Description"),
        max_length=255,
        default='',
        blank=True)

    featured_image_credit = models.CharField(
        verbose_name=_("Image Credit"),
        max_length=255,
        default='',
        blank=True)

    facebook_image = models.ForeignKey(
        MediaItem,
        null=True,
        blank=True,
        related_name="article_with_facebook_image",
        help_text='Image size should be 600 x 315 '
                  'for best results (or 1200 x 630 for high resolution)'
    )

    show_subscription_form = models.BooleanField(
        verbose_name=_("Show Subscription Form"),
        default=True)

    creator = models.ForeignKey(User, verbose_name="Creator")

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        permissions = (
            ("can_change_article_status", "Can change status of articles"),
        )
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ('order', )

    def __str__(self):
        return u'{0}: {1}'.format(self.get_custom_post_type_title(), self.title)

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


    def partners_limited(self):
        return Partner._partners(self)

    def get_custom_post_type_title(self):
        if self.news_analysis:
            return "Politics"
        else:
            post_types_dict = {
                list_item[0]: list_item[1]
                for list_item in CUSTOM_POST_TYPE_CHOICES}
            return post_types_dict[self.custom_post_type]

    def get_authors(self, link=True):
        """
        Return a comma separated list of authors as HTML links.
        """
        bio_url = '/about/staff/'

        names = []

        if self.guest_author:
            names.append(self.guest_author)

        for auth in self.authors.all():
            name = auth.full_name
            if link:
                slug = name.lower().replace(' ', '-')
                url = '<a href="{0}{1}" title="{2}">{2}</a>'.format(
                    bio_url, slug, name)
                names.append(url)
            else:
                names.append(name)

        if not names:
            return False

        return ', '.join(names)

    def post_type_link(self, link=True):
        """
        Return an HTML link to the post type feed.
        """

        if self.custom_post_type == 'external':
            return self.custom_source.upper()
        else:
            url = self.get_post_type_url()
            title = 'More {0} posts'.format(self.custom_post_type)
            text = self.custom_post_type.upper()
            return '<a href="{0}" title="More {1} posts">{2}</a>'.format(
                url, title, text)

    def get_absolute_url(self):
        url_name = "article_detail"
        kwargs = {
            "slug": self.slug,
        }
        return reverse(url_name, kwargs=kwargs)

    def _get_ordered_related_articles(self, published_only):
        """Get headlines in order of RelatedHeadlineArticle.order"""

        qs = RelatedArticle.objects.filter(
            related_article=self).select_related('article')

        # Todo:  Dry this out, this is duplicated in Publishable.
        if published_only:
            qs.filter(
                Q(article__publish_date__lte=now()) |
                Q(article__publish_date__isnull=True),
                Q(article__status=CONTENT_STATUS_PUBLISHED)).order_by(
                '-publish_date')

        return [a.article for a in qs.all()]

    def get_published_ordered_related_articles(self):
        return self._get_ordered_related_articles(published_only=True)

    def get_ordered_related_articles(self):
        return self._get_ordered_related_articles(published_only=False)

    def get_post_type_url(self):
        if self.custom_post_type != 'articles':
            return reverse('article_list_custom_post_type',
                           kwargs={'custom_post_type': self.custom_post_type})
        else:
            if self.news_analysis:
                return '/category/news-analysis/'
            else:
                return '/articles/'

    def get_social_title(self):
        """
        Return `self.social_title` if it exists. Else return `self.title`.
        """
        if self.social_title:
            return self.social_title
        else:
            return self.title

    # These methods are deprecated wrappers for keyword and category
    # access. They existed to support Django 1.3 with prefetch_related
    # not existing, which was therefore manually implemented in the
    # blog list views. All this is gone now, but the access methods
    # still exist for older templates.

    def category_list(self):
        from warnings import warn
        warn("blog_post.category_list in templates is deprecated"
             "use blog_post.categories.all which are prefetched")
        return getattr(self, "_categories", self.categories.all())

    def keyword_list(self):
        from warnings import warn
        warn("blog_post.keyword_list in templates is deprecated"
             "use the keywords_for template tag, as keywords are prefetched")
        try:
            return self._keywords
        except AttributeError:
            keywords = [k.keyword for k in self.keywords.all()]
            setattr(self, "_keywords", keywords)
            return self._keywords


    def get_post_type(self):
        return self.custom_post_type if self.custom_post_type else 'Article'

    def get_placeholder_atoms_for_sidebar(self):
        code_pattern = r'\[\satom\s(\d+)\sdisplay\=(?:text|image)\s?\]'
        incontent_atom_ids = re.findall(code_pattern, self.content)
        atoms = self.atoms.in_bulk(incontent_atom_ids)
        return map(lambda _id: atoms[int(_id)], incontent_atom_ids)

    def get_noncontent_atoms(self):
        code_pattern = r'\[\satom\s(\d+)\sdisplay\=[a-zA-Z]+\s?\]'
        content_atom_ids = re.findall(code_pattern, self.content)
        return self.atoms.exclude(pk__in=content_atom_ids)

    def get_atom_display_type(self, atom):
        # try to get display type from shortcode, else use default
        code_pattern = r'\[\satom\s' + str(atom.id)
        code_pattern += '\sdisplay\=([a-zA-Z]+)\s?\]'
        display_type = re.findall(code_pattern, self.content)
        if(display_type):
            return display_type[0]
        else:
            return atom.default_display_type

    def get_processed_content(self):

        """
        Applies all necessary text processing to blog post content
        and returns it for display.
        """

        # Copy content to ensure processing is non-destructive.
        content = copy(self.content)
        # Process named shortcodes

        #  Todo:  Reimplement when subscription is added back in
        content = self.process_shortcode_subscription_form(content)

        # Process atom shortcodes.
        content = self.process_atom_shortcodes(content)
        # Other processing here, if ever needed...
        return content
    processed_content = property(get_processed_content)

    #  Todo:  Reimplement when subscription is added back in
    def process_shortcode_subscription_form(self, text):

        # we need a subscription object for the template below
        # from subscription.forms import SubscribeForm
        # subscribe = SubscribeForm(None, article_slug=self.slug)

        # replace the shortcode, sending in the variables needed
        found, text = self.process_shortcode(
            text,
            'subscription_form',
            'subscription/shortcode_subscription_form.html',
            dict(article_slug=self.slug)
        )

        # if found in the content, don't show at bottom of page
        if found:
            self.show_subscription_form = False

        return text

    @staticmethod
    def process_shortcode(text, code_name, template_path, context_dict=None):

        """
        Replaces all instances of an editorial tag with a given template.
        """

        code_pattern = r'\[\s?%s\s?\]' % code_name
        shortcodes = re.findall(code_pattern, text)
        found = False

        if shortcodes:
            found = True
            shortcode = shortcodes[0]
            t = get_template(template_path)
            if context_dict:
                c = Context(context_dict)
            else:
                c = Context()
            shortcode_html = t.render(c)
            # debug_print_to_output(shortcode_html)
            # replace if p tags
            text = text.replace('<p>{0}</p>'.format(shortcode), shortcode_html)
            # replace if normal
            text = text.replace(shortcode, shortcode_html)

        return found, text

    def process_atom_shortcodes(self, text):

        """
        Replaces all instances of an editorial tag with a given template.
        """

        ATOM_SHORTCODE_NAME = 'atom'
        ATOM_SHORTCODE_TEMPLATE_PATH = (
            'includes/bits/post_atom_incontent.html')
        code_pattern = r'\[\s?{0}\s\d+\sdisplay\=[A-Za-z]+\s?\]'.format(
            ATOM_SHORTCODE_NAME)
#         clean_pattern = r'\<p\>\s?{0}\s?\<\/p\>'.format(code_pattern)
        atom_shortcodes = re.findall(code_pattern, text)

        if atom_shortcodes:
            for i, atom_shortcode in enumerate(atom_shortcodes):
                # extract the ID from the shortcode pattern.
                id_pattern = r'\d+'
                id_matches = re.findall(id_pattern, atom_shortcode)
                atom_id = id_matches[0] if id_matches else None
#                 print 'ID: {0}'.format(atom_id)
                # extract the display tpye from the shortcode pattern.
                display_pattern = r'(?<=display\=)[A-Za-z]+'
                display_matches = re.findall(display_pattern, atom_shortcode)
                atom_display_type = None
                if display_matches:
                    atom_display_type = display_matches[0]
                # Get the atom corresponding to ID from blog post's child atoms.

                try: # If atom, retrieve code with template.
                    atom = self.atoms.get(id=atom_id)
                    t = get_template(ATOM_SHORTCODE_TEMPLATE_PATH)
                    c = Context({
                        'atom': atom,
                        'display_type': atom_display_type,
                        'post': self})
                    shortcode_html = t.render(c)
                    shortcode_html = shortcode_html
                except Exception as e:
                    shortcode_html = ''
                text = text.replace(atom_shortcode, shortcode_html)
                # Remove <p> tags wraped around inserted div.
                text = text.replace(
                    '<p>{0}</p>'.format(shortcode_html), shortcode_html)

        return text

    def filtered_partners(self):
        partner_dict = Partner._partners(self)
        return partner_dict['chosen_partners'].union(
            set(pa.partner for pa in partner_dict['other_partners']))
