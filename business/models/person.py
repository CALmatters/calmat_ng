from django.contrib.auth.models import User
from django.db import models

from media_manager.models import MediaItem
from sites.models import Named, TimeStamped
from sites.models.content_container import OptionalContentContainer


class Person(Named, TimeStamped, OptionalContentContainer):

    exerpt = models.TextField("Excerpt", blank=True, null=True)

    staff_member = models.BooleanField(
        default=False, help_text="Staff/Team member")
    director_board_member = models.BooleanField(
        default=False, help_text="On Board of Directors")
    advisory_board = models.BooleanField(
        default=False, help_text="On Advisory Board")

    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        help_text='Connects the `Person` object to a `User` that can log in '
                  'If no `User` is selected, you can supply names and '
                  'email below',)

    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    email = models.EmailField('email address', blank=True)

    job_title = models.CharField(
        max_length=100,
        default='',
        blank=True
    )

    image = models.OneToOneField(
        MediaItem, null=True, blank=True, related_name="person")

    twitter = models.CharField(
        verbose_name='Twitter @',
        max_length=256,
        default='',
        blank=True,
        help_text="Adding a Facebook url will enable Facebook authoring.  "
                  "i.e. https://www.facebook.com/your_name")

    facebook_url = models.CharField(
        verbose_name='Facebook URL',
        max_length=256,
        default='',
        blank=True,
        help_text="Adding a Facebook url will enable Facebook authoring.  "
                  "i.e. https://www.facebook.com/your_name")

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def get_absolute_url(self):
        # Todo:  When there's a Author landing page.
        return '/about/staff/{}/'.format(self.slug)

    def __str__(self):
        s = self.full_name
        if not s:
            s = self.username
        return s

    @property
    def username(self):
        if self.user:
            return self.user.username
        else:
            ""

    @property
    def full_name(self):
        return "{0} {1}".format(
            self.first_name, self.last_name).strip()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        try:
            self.first_name = self.first_name or self.user.first_name
            self.last_name = self.last_name or self.user.last_name
            self.email = self.email or self.user.email
        except AttributeError:
            pass

        self.title = self.full_name
        super(Person, self).save(
            force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ('order', )
