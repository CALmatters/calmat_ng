from django.contrib.auth.models import User
from django.db import models

from media_manager.models import MediaItem
from sites.models import Named, Publishable, TimeStamped


class Person(Named, TimeStamped):

    user = models.OneToOneField(
        User,
        help_text='Connects the `author` object to a `User`'
                  'to pull in the profile photo on a post.',)

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

    def get_absolute_url(self):
        # Todo:  When there's a Author landing page.
        return '/'

    def __str__(self):
        s = self.full_name
        if not s:
            s = self.username
        return s

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return "{0} {1}".format(
            self.user.first_name, self.user.last_name).strip()

    def save(self, *args, **kwargs):
        self.title = self.full_name
        super(Named, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'