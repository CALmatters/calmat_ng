from django.core.checks import messages
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from adminsortable2.admin import SortableInlineAdminMixin

from pages.models import HomePage

from pages.models.homepage import RelatedHeadlineArticle, RelatedAtom


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


class RelatedAtomInline(SortableInlineAdminMixin, TabularInline):
    model = RelatedAtom
    fields = ('atom', 'atom_layout', 'order')
    exlude= ('article', )
    extra = 0


class HomePageAdmin(admin.ModelAdmin):

    class Media:
        js = ()
        css = {
            'all': (
                'theme/frontend/css/font-awesome-4.5.0/css/font-awesome.css',
            )
        }

    list_display = [
        "title",
        "can_go_live",
        "go_live_on_date",
        "current_live",
        "preview"
    ]
    readonly_fields = ('slug',)
    list_editable = ('can_go_live', )

    list_filter = (
        "can_go_live",
    )

    actions = (clone, )

    inlines = (RelatedHeadlineArticleInline, RelatedAtomInline)

    fieldsets = (
        (None, {
            "fields": (
                "title",
                "can_go_live",
                "go_live_on_date",
            )
        }),
        ("General", {
            "fields": (
                "masthead_copy",
            )
        }),
        ("In the Works", {
            "fields": (
                ("works_display_one", "works_url_one",),
                ("works_display_two", "works_url_two",),
                ("works_display_three", "works_url_three", ),
                ("works_display_four", "works_url_four", ),
                ("works_display_five", "works_url_five", )
            )
         }),
        ("Main Articles", {
            "fields": (
                "primary_article",
                "secondary_article_left",
                "secondary_article_right",
            )
        }),
        ("The Basics - Four links that live in right sidebar", {
            "fields": (
                "the_basics_one",
                "the_basics_two",
                "the_basics_three",
                "the_basics_four",
            )
        }),
        ("Politics", {
            "fields": (
                "politics_author",
                "politics_quote"
            )
        }),

    )

    def preview(self, obj):
        return mark_safe(
            "<a target='_blank' href={}>Click to view "
            "<i class='fa fa-external-link' aria-hidden='true'>"
            "</i></a>".format(reverse(
                'home_page_preview', args=(obj.id,)), obj.title))
    preview.short_description = "Preview HomePage "

    def current_live(self, obj):

        try:
            live_obj = HomePage.objects.get_live_object()
        except IndexError:
            live_obj = None

        if not obj.can_go_live:
            return ""
        elif live_obj and obj == live_obj:
            return 'CURRENT LIVE HOMEPAGE'
        elif obj.go_live_on_date < now():
            return ""
        elif obj.go_live_on_date > now():
            dt = obj.go_live_on_date - now()
            return "{} days, {} hours, {} minutes TO LIVE".format(
                dt.days, int(dt.seconds / 3600), dt.seconds % 60)

    current_live.short_description = "Live Status"

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