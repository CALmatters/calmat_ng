
from django.db import models
from django.core.urlresolvers import reverse

# from versatileimagefield.fields import VersatileImageField
from fkchooser.fields import PopupForeignKey
from media_manager.models import MediaItem
from sites.models import Named, TimeStamped, Publishable

from business.models import Partner
from categories.models import Category
from pages.models import Article, Atom, Quote

PROJECT_ATOM_LAYOUT_CHOICES = (
    ('image-headline', 'Image + Headline'),
    ('image', 'Featured Image Only'),
    ('atom-block', 'Atom Block'),
    ('embedded', 'Embeded Content <iframe>'),
)


class Project(Named, Publishable, TimeStamped):

    # featured_image = VersatileImageField(
    #     verbose_name="Old Featured Image",
    #     upload_to="project_images/",
    #     null=True,
    #     blank=True
    # )

    image = models.ForeignKey(
        MediaItem,
        verbose_name="Featured Image",
        null=True,
        blank=True,
        related_name="aproject_with_image")

    # Top featured articles
    features = models.ManyToManyField(
        Article,
        verbose_name='Featured Articles',
        through='ProjectSortableFeaturedArticle',
        related_name='projects_showing_article_as_feature',
        blank=True,
    )

    # OnRamp area at top left
    onramp = models.ForeignKey(
        "OnRamp",
        verbose_name='Project OnRamp',
        related_name='projects_showing_onramp',
        help_text='Appears on the left.',
        blank=True,
        null=True,
    )

    # Atom area at top right
    atom = models.ForeignKey(
        Atom,
        verbose_name='Project Atom',
        related_name='projects_showing_atom',
        help_text='Appears on the right.',
        blank=True,
        null=True,
    )

    atom_layout = models.CharField(
        max_length=20,
        choices=PROJECT_ATOM_LAYOUT_CHOICES,
        default='image-headline',
        help_text='Atom layout',
    )

    visualizations = models.ManyToManyField(
        Atom,
        verbose_name='Visualizations',
        related_name='visualizations',
        through='ProjectSortableVisualizations',
        blank=True,
    )

    quotes = models.ManyToManyField(
        Quote,
        verbose_name='Quotes',
        through='ProjectSortableQuotes',
        related_name='projects_showing_quote',
        blank=True,
    )

    # Bottom related stories (which are blog.BlogPost, not theme.Story)
    related_articles = models.ManyToManyField(
        Article,
        verbose_name='Related Articles',
        through='ProjectSortableRelatedArticle',
        related_name='projects_showing_article_as_related',
        blank=True,
    )

    expert_perspectives_articles = models.ManyToManyField(
        Article,
        verbose_name='Expert Perspectives Articles',
        through='ProjectSortableExpertPerspectivesArticle',
        related_name='projects_showing_article_as_expert_perspective',
        blank=True,
    )

    reader_reactions_articles = models.ManyToManyField(
        Article,
        verbose_name='Reader Reactions Articles',
        through='ProjectSortableReaderReactionsArticle',
        related_name='projects_show_article_as_reader_reaction',
        blank=True,
    )

    updates_articles = models.ManyToManyField(
        Article,
        verbose_name='Updates Articles',
        through='ProjectSortableUpdatesArticles',
        related_name='projects_showing_article_as_update',
        blank=True,
    )

    # Partner logos to include
    partners = models.ManyToManyField(
        Partner,
        verbose_name='Partners for project',
        through="ProjectSortablePartners",
        related_name='projects_for_partner',
        blank=True,
    )

    # Categories used for Related Stories
    categories = models.ManyToManyField(
        Category,
        verbose_name="Categories",
        blank=True,
        related_name="projects"
    )

    # Storify url
    storify_embed = models.TextField(
        verbose_name="Storify Embed",
        default='',
        blank=True
    )

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        permissions = (
            ("can_change_project_status", "Can change status of projects"),
        )
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ('order', '-publish_date',)

    def get_category_ids(self):
        """
        Return a list of category IDs
        """
        cats = self.categories.all()
        cat_ids = [c.id for c in cats]
        if cat_ids:
            return cat_ids
        else:
            # get all category ids
            cat_ids = Category.objects.all().values('id')
            cat_ids = [c['id'] for c in cat_ids]
            return cat_ids

    def get_absolute_url(self):
        url_name = "project_detail"
        kwargs = {
            "slug": self.slug,
        }
        return reverse(url_name, kwargs=kwargs)

    @staticmethod
    def get_display_projects(request=None):

        if request is not None and request.user.is_staff:
            return Project.objects.all()
        else:
            return Project.objects.published()


class OrderedManager(models.Manager):

    def __init__(self, join_field, *args, **kwargs):
        super(OrderedManager, self).__init__(*args, **kwargs)
        self.join_field = join_field

    def ordered_for_project(self, project):
        return [getattr(t, self.join_field) for t in self.filter(
            project=project).order_by('order').select_related(self.join_field)]


class ProjectArticleSortableBase(models.Model):

    """
    Base Joining Class joining Stories to Article
    Contributes a order field to be used to order the relations
    The order is managed in the admin through Django-admin-stortable2
    """

    project = models.ForeignKey(Project)
    article = PopupForeignKey(Article)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    objects = OrderedManager('article')

    class Meta:
        abstract = True


class ProjectSortableFeaturedArticle(ProjectArticleSortableBase):
    """Concrete class joining project to article"""

    class Meta:
        ordering = ('order',)
        verbose_name = "Featured Article"
        verbose_name_plural = "Featured Articles"


class ProjectSortableRelatedArticle(ProjectArticleSortableBase):

    class Meta:
        ordering = ('order',)
        verbose_name = "Related Article"
        verbose_name_plural = "Related Article"


class ProjectSortableExpertPerspectivesArticle(ProjectArticleSortableBase):

    class Meta:
        ordering = ('order',)
        verbose_name = "Expert Perspective Article"
        verbose_name_plural = "Expert Perspectives Articles"


class ProjectSortableReaderReactionsArticle(ProjectArticleSortableBase):

    class Meta:
        ordering = ('order',)
        verbose_name = "Reader Reaction Article"
        verbose_name_plural = "Reader Reactions Articles"


class ProjectSortableUpdatesArticles(ProjectArticleSortableBase):

    class Meta:
        ordering = ('order',)
        verbose_name = "Update Articles"
        verbose_name_plural = "Updates Articles"


class ProjectSortableQuotes(models.Model):

    project = models.ForeignKey(Project)
    quote = models.ForeignKey(Quote)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    objects = OrderedManager('quote')

    class Meta:
        ordering = ('order',)
        verbose_name = "Project Quote"
        verbose_name_plural = "Project Quotes"


class ProjectSortableAtomBase(models.Model):
    project = models.ForeignKey(Project)
    atom = PopupForeignKey(Atom)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    objects = OrderedManager('atom')

    class Meta:
        ordering = ('order',)
        abstract = True


class ProjectSortableVisualizations(ProjectSortableAtomBase):

    class Meta:
        ordering = ('order',)
        verbose_name = "Infograph"
        verbose_name_plural = "Infographs"


class ProjectSortablePartnerBase(models.Model):
    project = models.ForeignKey(Project)
    partner = models.ForeignKey(Partner)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    objects = OrderedManager('partner')

    class Meta:
        abstract = True


class ProjectSortablePartners(ProjectSortablePartnerBase):

    class Meta:
        ordering = ('order',)
        verbose_name = "Partner"
        verbose_name_plural = "Partners"
