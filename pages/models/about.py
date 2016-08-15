from django.db import models

from business.models import Partner, Person
from cmskit.models import TimeStamped


class AboutPartner(models.Model):

    about = models.ForeignKey('About')
    partner = models.ForeignKey(Partner)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = "Partner Logo"
        verbose_name_plural = "Partner Logos"
        ordering = ('order',)


class About(TimeStamped):

    name = models.CharField(
        max_length=50,
        help_text="Used for internal tracking only.")

    tagline = models.CharField(
        verbose_name='CALmatters tagline',
        max_length=200,
        blank=True)

    mission  = models.TextField(
        verbose_name='Mission',
        blank=True,
        default="",
        help_text='Content for the Mission section of the About page.')

    team = models.TextField(
        verbose_name='Team',
        blank=True,
        default="",
        help_text='Left content for the Team section of the About page.')

    partners = models.TextField(
        verbose_name='Partners',
        blank=True,
        default="",
        help_text='Left content for the Partners section of the About page.')

    funders  = models.TextField(
        verbose_name='Funders/Supporters',
        blank=True,
        default="",
        help_text='Left content for the Funders/Supporters '
                  'section of the About page.')

    funders_list  = models.TextField(
        verbose_name='Funders Names',
        blank=True,
        default="",
        help_text='List of names for the right hand '
                  'section of Funders/Supporters.')

    partner_logos = models.ManyToManyField(
        Partner,
        blank=True,
        verbose_name='Partner Logos',
        through='AboutPartner')

    donate_message = models.CharField(max_length=300, blank=True)
    jobs_message = models.CharField(max_length=300, blank=True)

    def get_absolute_url(self):
        raise NotImplementedError()

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Pages"
        get_latest_by = 'created'
