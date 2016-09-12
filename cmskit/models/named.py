from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.text import slugify


def unique_slug(queryset, slug_field, slug):
    """
    Ensures a slug is unique for the given queryset, appending
    an integer to its end until the slug is unique.
    """
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit("-", 1)[0]
            slug = "%s-%s" % (slug, i)
        try:
            queryset.get(**{slug_field: slug})
        except ObjectDoesNotExist:
            break
        i += 1
    return slug


class Named(models.Model):
    """

    Todo:  Should be a mixin that required some field be nominated as a
    title, a description and a slug.  And, be able to supress the requirement
    if you don't want a field, like you want title adn slug, but no description.
    This could the basis for less classes.

    """

    class Meta:
        abstract = True

    #  Todo:  short_decription a better more general name
    title = models.CharField(_("Title"), max_length=500)
    description = models.TextField(
        "Description (135 Chars)", max_length=135, blank=True, default='')

    reverse_name = None

    slug = models.CharField(
        "Slug",
        max_length=2000,
        blank=True,
        null=True,
        help_text=_("Auto-generated from the title when blank.  "
                    "slug is used in the url that relates to this content"))

    def generate_unique_slug(self):
        """
        Create a unique slug by passing the result of get_slug() to
        utils.urls.unique_slug, which appends an index if necessary.
        """
        # For custom content types, use the ``Page`` instance for
        # slug lookup.

        slug_qs = self.__class__.objects.exclude(id=self.id)
        return unique_slug(slug_qs, "slug", self.get_slug())

    def get_slug(self):
        """
        Allows subclasses to implement their own slug creation logic.
        """

        # Todo: If allow_unicode=True is a problerm, remove it.
        # Todo: Prob don't need it
        return slugify(self.title, allow_unicode=True)

    def get_absolute_url(self):
        if hasattr(self, 'url_name') and self.url_name:
            kwargs = {
                "slug": self.slug,
            }
            return reverse(self.url_name, kwargs=kwargs)

    def view_url(self):
        """Admin function for list_display or fieldsets"""

        if self.slug:
            url = reverse(self.reverse_name, kwargs=dict(slug=self.slug))
            return mark_safe(
                "<a href={url} target='_blank'>"
                "<i class='fa fa-open'></i>{slug}</a>".format(
                    url=url, slug="CLICK TO VIEW"))
        else:
            return ""
    view_url.short_description = "View in browser"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        If no slug is provided, generates one before saving.
        """
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(Named, self).save(
            force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title
