from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from business.models.partner_article import PartnerArticle
from pages.models import Article
from pages.models.article import RelatedArticle


def clone(modeladmin, request, queryset):

    for article in queryset.all():
        article.clone()
clone.short_description = "Duplicate"


class RelatedArticleInline(SortableInlineAdminMixin, TabularInline):
    model = RelatedArticle
    fk_name = 'article'
    fields = (
        'title', 'order')
    max_num = 100
    extra = 0


class PartnerArticleInline(SortableInlineAdminMixin, TabularInline):
    model = PartnerArticle
    fields = (
        'partner', 'fulltext_or_mention', 'date_published', 'url', 'order')
    max_num = 100
    extra = 0


#  Todo:  Twitter support
class ArticleAdmin(SortableAdminMixin, admin.ModelAdmin):

    # Todo:  Move to Admin super class parallel with ContentContainer is Sites
    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.min.js',
            'theme/js/tinymce_ng.js'
        )
        css = {
            'all': (
                )
        }

    actions = [clone]

    list_display = [
        "title",
        "status",
        "publish_date",
        "custom_post_type",
        "news_analysis",
        "category_list",
        "creator",
        "authors_list",
        # "atoms_list",
        # "admin_thumb",
        # "admin_link"
    ]
    readonly_fields = ('slug', )
    list_editable = ('status', 'news_analysis')

    list_filter = (
        "status",
        # "keywords__keyword",
        "custom_post_type",
        "news_analysis",
        "atoms",
        # "partners",
        "authors")

    inlines = (
        RelatedArticleInline,
        PartnerArticleInline,
    )

    filter_horizontal = (
        "categories", "related_posts", "atoms", "authors",)

    fieldsets = (
        ("Control", {
            "fields": (
                "status",
                "custom_post_type",
                "slug",
                "news_analysis",
                "publish_date",
            )
        }),
        ("General", {
            "fields": (
                "title",
                "social_title",
                "description",
                "headline_layout",

            )
        }),
        (_("Content and Images"), {
            # "classes": ("collapse-closed",),
            "fields": (
                "content",
                "featured_image",
                "featured_image_description",
                "featured_image_credit",
                "featured_image_title_position",
                "featured_image_title_shade",
                "facebook_share_image",
            )
        }),
        (_("Layout"), {
            # "classes": ("collapse-open",),
            "fields": ("layout",)
        }),
        (_("Authors"), {
            "classes": ("collapse-open",),
            "fields": (
                "authors",
                "guest_author"
            )
        }),
        (_("Tagging"), {
            # "classes": ("collapse-open",),
            "fields": (
                "categories",
            )
        }),
        (_("Related Content"), {
            "classes": ("collapse-open",),
            "fields": (
                "atoms",
                # "related_persons",
            )
        }),
        (_("External Info"), {
            # "classes": ("collapse-closed",),
            "fields": (
                "custom_source",
                "custom_link",)
        }),
    )

    def category_list(self, obj):
        """Used in list_display above."""
        return ', '.join([c.title for c in obj.categories.all()])
    category_list.short_description = "Categories"

    def authors_list(self, obj):
        authors = []
        if obj.guest_author:
            authors.append(obj.guest_author)

        if obj.authors.exists():
            for a in obj.authors.all():
                authors.append(a.full_name)
        if authors:
            return ', '.join(authors)
        else:
            return ''
    authors_list.short_description = 'Authors'

    def atoms_list(self, obj):
        if obj.atoms.exists():
            return ', '.join([a.title for a in obj.atoms.all()])
        else:
            return ''
    atoms_list.short_description = 'Atoms'

    def save_form(self, request, form, change):
        obj = form.save(commit=False)
        if obj.creator is None:
            obj.creator = request.user
        return super(ArticleAdmin, self).save_form(request, form, change)

admin.site.register(Article, ArticleAdmin)
