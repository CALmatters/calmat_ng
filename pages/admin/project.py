from django.contrib import admin
from django import forms

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib.admin import TabularInline

from cmskit.mixins.cloneable import Cloneable
from media_manager.widgets import PopupSelect
from pages.models.project import (Project, ProjectSortableFeaturedArticle,
                                  ProjectSortableRelatedArticle,
                                  ProjectSortableQuotes,
                                  ProjectSortablePartners,
                                  ProjectSortableVisualizations,
                                  ProjectSortableExpertPerspectivesArticle,
                                  ProjectSortableReaderReactionsArticle,
                                  ProjectSortableUpdatesArticles)
from cmskit.mixins.admin_thumb import AdminThumbMixin

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


class ProjectAdmin(Cloneable, SortableAdminMixin, AdminThumbMixin, admin.ModelAdmin):

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

    # filters in right column
    list_filter = ("categories",)

    fieldsets = (
        ('Title',
         {'fields': (
             'title', 'slug', 'status', 'publish_date', 'image')}),
        ('Content', {'fields': ('description',)}),
        ('OnRamp and Atom', {'fields': ('onramp', 'atom', 'atom_layout',)}),
        ('Categories', {'fields': ('categories',)}),
    )

    admin_thumb_ref = "image"
    admin_thumb_field = 'file'

    def get_readonly_fields(self, request, obj=None):
        extra_ro = ()
        if not request.user.has_perm('pages.can_change_project_status'):
            extra_ro = ('status', 'publish_date')

        if not obj or obj.is_published:
            extra_ro = extra_ro + ('slug',)

        return self.readonly_fields + extra_ro

admin.site.register(Project, ProjectAdmin)
