from django.db import models

from business.models import Partner
from fkchooser.fields import PopupForeignKey
from pages.models import Article

FULL_OR_MENTION_CHOICES = (
    ('Not Specified', 'Not Specified'),
    ('Full Text Publish', 'Full Text Publish'),
    ('Mention/Aggregation', 'Mention/Aggregation'))
DEFAULT_FULL_OR_MENTION_CHOICES = FULL_OR_MENTION_CHOICES[1][0]


class PartnerArticle(models.Model):

    class Meta:
        verbose_name = "Distribution"
        verbose_name_plural = "Distributions"
        unique_together = ('article', 'partner', 'date_published', 'notes')
        ordering = ('order', )

    article = PopupForeignKey(Article)

    partner = models.ForeignKey(Partner)

    fulltext_or_mention = models.CharField(
        verbose_name="Publish Type",
        max_length=len(max((v[0] for v in FULL_OR_MENTION_CHOICES), key=len)),
        choices=FULL_OR_MENTION_CHOICES,
        default=DEFAULT_FULL_OR_MENTION_CHOICES
        )

    date_published = models.DateField(blank=True, null=True)

    url = models.CharField(max_length=255, blank=True, default='')

    file_upload = models.FileField(
        upload_to="uploads/published", blank=True, null=True)

    print_publish = models.NullBooleanField()

    radio_broadcast = models.NullBooleanField(default=False)

    properly_credited = models.NullBooleanField(
        verbose_name="Properly credited?",
        default=True)

    notes = models.TextField(blank=True, default='')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return u"%s (%s)" % (self.article, self.partner)