from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Q

CONTENT_STATUS_DRAFT = 1
CONTENT_STATUS_PUBLISHED = 2
CONTENT_STATUS_CHOICES = (
    (CONTENT_STATUS_DRAFT, _("Draft")),
    (CONTENT_STATUS_PUBLISHED, _("Published")),
)


class PublishableManager(models.Manager):
    """
    Provides filter for restricting items returned by status and
    publish date when the given user is not a staff member.
    """

    def published(self, for_user=None):
        """
        For non-staff users, return items with a published status and
        whose publish and expiry dates fall before and after the
        current date when specified.
        """

        if for_user is not None and for_user.is_staff:
            return self.all().order_by('-publish_date')
        return self.filter(
            Q(publish_date__lte=now()) | Q(publish_date__isnull=True),
            Q(status=CONTENT_STATUS_PUBLISHED)).order_by('-publish_date')


class Publishable(models.Model):

    class Meta:
        abstract = True

    status = models.IntegerField(
        _("Status"),
        choices=CONTENT_STATUS_CHOICES,
        default=CONTENT_STATUS_DRAFT,
        help_text=_("With Draft chosen, will only be shown for "
                    "admin users on the site."))

    publish_date = models.DateTimeField(
        _("Published from"),
        help_text=_("With Published chosen, won't be shown until this time"),
        blank=True,
        null=True)

    @property
    def is_published(self):
        published_by_date = self.publish_date and self.publish_date < now()
        published_by_flag = self.status == CONTENT_STATUS_PUBLISHED
        print(published_by_date)
        print(published_by_flag)
        return published_by_date or published_by_flag

    objects = PublishableManager()
