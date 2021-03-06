from django import forms

from django.core.urlresolvers import reverse
from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.safestring import mark_safe

from adminsortable2.admin import SortableInlineAdminMixin

from business.models.partner_article import PartnerArticle
from fkchooser.admin import FKChooserAdminMixin
from media_manager.widgets import PopupSelect
from pages.models import Article
from pages.models.article import RelatedArticle
from cmskit.mixins.admin_thumb import AdminThumbMixin


def clone(modeladmin, request, queryset):
    for article in queryset.all():
        article.clone()
clone.short_description = "Duplicate"


class RelatedArticleInline(SortableInlineAdminMixin, TabularInline):
    model = RelatedArticle
    fk_name = 'related_article'
    fields = (
        'article', 'related_article', 'order')
    max_num = 3
    extra = 0


class PartnerArticleInline(SortableInlineAdminMixin, TabularInline):
    model = PartnerArticle
    fields = (
        'partner', 'fulltext_or_mention', 'date_published', 'url', 'order')
    max_num = 100
    extra = 0


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        widgets = {
            'image': PopupSelect(),
            'facebook_image': PopupSelect(),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
        exclude = ()


#  Todo:  Twitter support
class ArticleAdmin(AdminThumbMixin, FKChooserAdminMixin, admin.ModelAdmin):

    form = ArticleAdminForm

    list_per_page = 20

    # Todo:  Move to Admin super class parallel with ContentContainer is Sites
    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.js',
            'theme/js/atom_chooser_plugin.js',
            'theme/js/image_file_picker.js',
            'theme/js/tinymce_ng_atoms.js',
            'js/copy_forward_image_data.js',

        )
        css = {
            'all': (
                )
        }

    actions = [clone]

    list_display = [
        "custom_post_type",
        "category_list",
        "title",
        "creator",
        "authors_list",
        "atoms_list",
        "status",
        "admin_thumb_reference",
        # "admin_link"
    ]

    list_display_links = ('title', )
    readonly_fields = ('view_url', )

    list_filter = (
        "categories",
        "status",
        "custom_post_type",
        "news_analysis",
        "authors",)

    search_fields = ('title', )

    inlines = (
        RelatedArticleInline,
        # PartnerArticleInline,
    )

    filter_horizontal = (
        "categories", "related_posts", "atoms", "authors",)

    fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "title",
                "slug",
                "social_title",
                "layout",
                "custom_post_type",
                "view_url",
                "news_analysis",
                ("status", "publish_date"),

            )
        }),
        (_("Featured Image"), {
            "classes": ("collapse-open",),
            "fields": (
                "headline_layout",
                "image",
                "featured_image_description",
                "featured_image_credit",
                "featured_image_title_position",
                "featured_image_title_shade",
                "facebook_image",
            )
        }),
        (_("Content"), {
            "fields": (

                "content",
            ),
            'classes': (
                "tinymce-editable",
            )
        }),
        (_("Description"), {
            "fields": (
                "description",
            ),
        }),
        (_("Authors"), {
            "classes": ("collapse-open",),
            "fields": (
                "authors",
                "guest_author"
            )
        }),
        (_("Categories"), {
            # "classes": ("collapse-open",),
            "fields": (
                "categories",
            )
        }),
        (_("Related Atoms"), {
            "classes": ("collapse-open",),
            "fields": (
                "atoms",
            )
        }),
        (_("External Info"), {
            "classes": ("collapse",),
            "fields": (
                "custom_source",
                "custom_link",)
        }),
    )

    admin_thumb_ref = "image"
    admin_thumb_field = 'file'

    def get_readonly_fields(self, request, obj=None):

        extra_ro = ()
        if not request.user.has_perm('pages.can_change_article_status'):
            extra_ro = ('status', 'publish_date')

        if not obj or obj.is_published:
            extra_ro = extra_ro + ('slug',)

        return self.readonly_fields + extra_ro

    def category_list(self, obj):
        """Used in list_display above."""
        return ', '.join([c.title for c in obj.categories.all()])
    category_list.short_description = "Categories"

    def view_url(self, obj):
        if obj.slug:
            url = reverse('article_detail', kwargs=dict(slug=obj.slug))
            return mark_safe(
                "View Article:  <a href={url}>{slug}</a>".format(
                    url=url, slug=obj.title))
        else:
            return ""
    view_url.short_description = "View Article"

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
        try:
            creator = obj.creator
        except:
            obj.creator = request.user
        else:
            if creator is None:
                obj.creator = request.user
        return super(ArticleAdmin, self).save_form(request, form, change)

admin.site.register(Article, ArticleAdmin)
