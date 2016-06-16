from django.contrib import admin
from django import forms

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib.admin import TabularInline

from media_manager.widgets import PopupSelect
from pages.models.project import (Project, ProjectSortableFeaturedArticle,
                                  ProjectSortableRelatedArticle,
                                  ProjectSortableQuotes,
                                  ProjectSortablePartners,
                                  ProjectSortableVisualizations,
                                  ProjectSortableExpertPerspectivesArticle,
                                  ProjectSortableReaderReactionsArticle,
                                  ProjectSortableUpdatesArticles)
from sites.mixins.admin_thumb import AdminThumbMixin

PROJECT_RELATED_ARTICLE_COUNT = 100


class ProjectSortableFeaturedInline(SortableInlineAdminMixin, TabularInline):
    model = ProjectSortableFeaturedArticle
    fields = ('article', 'order')
    max_num = 100


class ProjectSortableQuotesInline(SortableInlineAdminMixin, TabularInline):
    model = ProjectSortableQuotes
    max_num = 100


class ProjectSortableRelatedArticleInline(SortableInlineAdminMixin,
                                          TabularInline):
    model = ProjectSortableRelatedArticle
    max_num = PROJECT_RELATED_ARTICLE_COUNT


class ProjectSortableExpertPerspectivesArticleInline(SortableInlineAdminMixin,
                                                     TabularInline):
    model = ProjectSortableExpertPerspectivesArticle
    max_num = 100


class ProjectSortableReaderReactionsArticleInline(SortableInlineAdminMixin,
                                                  TabularInline):
    model = ProjectSortableReaderReactionsArticle
    max_num = 100


class ProjectSortableUpdatesArticlesInline(SortableInlineAdminMixin,
                                           TabularInline):
    model = ProjectSortableUpdatesArticles
    max_num = 100


class ProjectSortableVisualizationsInline(SortableInlineAdminMixin,
                                          TabularInline):
    model = ProjectSortableVisualizations
    max_num = 100


class ProjectSortablePartnersInline(SortableInlineAdminMixin, TabularInline):
    model = ProjectSortablePartners
    max_num = 100


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            'image': PopupSelect(),
        }
        exclude = ()


class ProjectAdmin(SortableAdminMixin, AdminThumbMixin, admin.ModelAdmin):

    form = ProjectAdminForm

    inlines = (
        ProjectSortableFeaturedInline,
        ProjectSortableQuotesInline,
        ProjectSortablePartnersInline,
        ProjectSortableRelatedArticleInline,
        ProjectSortableVisualizationsInline,
        ProjectSortableExpertPerspectivesArticleInline,
        ProjectSortableReaderReactionsArticleInline,
        ProjectSortableUpdatesArticlesInline,
    )

    list_display = (
        'title', 'slug', 'status', 'publish_date', 'admin_thumb_reference')
    filter_horizontal = ('categories', 'partners')
    readonly_fields = ('slug', 'order')

    # filters in right column
    list_filter = ("categories",)

    fieldsets = (
        ('Title',
         {'fields': (
             'title', 'status', 'publish_date', 'image')}),
        ('Content', {'fields': ('description',)}),
        ('OnRamp and Atom', {'fields': ('onramp', 'atom', 'atom_layout',)}),
        ('Categories', {'fields': ('categories',)}),
    )

    admin_thumb_ref = "image"
    admin_thumb_field = 'file'

admin.site.register(Project, ProjectAdmin)
