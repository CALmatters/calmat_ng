from django.core.checks import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.admin import TabularInline

from adminsortable2.admin import SortableInlineAdminMixin

from pages.models import HomePage

from pages.models.homepage import RelatedHeadlineArticle
from sites.models.publishable import (CONTENT_STATUS_DRAFT,
                                      CONTENT_STATUS_PUBLISHED)

# Todo:  Fix this.  It shouldn't take anything thin the queryset
# Todo:  This should find the latest one and publish it. - needs work

# Todo:  Publishing will be done through publish date, update this.
# Todo:  publishing should cause the publish date to be set to now()
# Todo:  And no other
def make_published(modeladmin, request, queryset):
    if queryset.count() != 1:
        msg = ("Only a single home page can be published at a time.  "
               "Please attempt to publish a single Home Page, "
               "all others will be set to draft.")
        modeladmin.message_user(request, msg, level=messages.WARNING)

    HomePage.objects.update(status=CONTENT_STATUS_DRAFT)

    homepage = queryset.all()[0]
    homepage.status = CONTENT_STATUS_PUBLISHED
    homepage.save()
make_published.short_description = "Publish Home Page"


def clone(modeladmin, request, queryset):
    if queryset.count() != 1:
        msg = "Only a single home page can be cloned at a time."
        modeladmin.message_user(request, msg, level=messages.WARNING)

    homepage = queryset.all()[0]
    homepage.clone()
clone.short_description = "Duplicate"


class RelatedHeadlineArticleInline(SortableInlineAdminMixin, TabularInline):
    model = RelatedHeadlineArticle
    exlude= ('article', 'order')
    max_num = 4
    extra = 0

class HomePageAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "status",
        "created",
        "updated",
    ]
    readonly_fields = ('slug',)
    list_editable = ('status', )

    list_filter = (
        "status",
    )

    actions = (make_published, clone)

    inlines = (RelatedHeadlineArticleInline, )

    fieldsets = (
        (None, {
            "fields": (
                "status",
                "title",
            )
        }),
        (_("General"), {
            "fields": (
                "masthead_copy",
            )
        }),
        (_("In the Works"), {
            "fields": (
                ("works_display_one", "works_url_one",),
                ("works_display_two", "works_url_two",),
                ("works_display_three", "works_url_three", ),
                ("works_display_four", "works_url_four", ),
                ("works_display_five", "works_url_five", )
            )
         }),
        (_("Main Articles"), {
            "fields": (
                "primary_article",
                "secondary_article_left",
                "secondary_article_right",
            )
        }),
        (_("The Basics"), {
            "fields": (
                "the_basics_one",
                "the_basics_two",
                "the_basics_three",
                "the_basics_four",
            )
        }),
    )




    # def category_list(self, obj):
    #     """Used in list_display above."""
    #     return ', '.join([c.title for c in obj.categories.all()])
    # category_list.short_description = "Categories"

    # def save_form(self, request, form, change):
    #     """
    #     Super class ordering is important here - user must get saved first.
    #     """
    #     OwnableAdmin.save_form(self, request, form, change)
    #     return DisplayableAdmin.save_form(self, request, form, change)

admin.site.register(HomePage, HomePageAdmin)