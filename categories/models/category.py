from django.db import models

from cmskit.models import Named
from cmskit.models import TimeStamped


class Category(Named, TimeStamped):

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    preferred = models.BooleanField(default=False)

    as_menu = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ('order',)

    @models.permalink
    def get_absolute_url(self):
        return "article_list_category", (), {"category": self.slug}

    @staticmethod
    def get_display_categories():
        if not hasattr(Category, '_categories'):
            r_cats = []
            for cat in Category.objects.filter(preferred=True):
                r_cats.append(dict(
                    id=cat.id,
                    url=cat.get_absolute_url(),
                    display_name=cat.title))

            Category._categories = r_cats

        return Category._categories

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        try:
            del Category._categories
        except AttributeError:
            pass


