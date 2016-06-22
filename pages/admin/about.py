from django.contrib import admin
from django.contrib.admin import TabularInline

from adminsortable2.admin import SortableInlineAdminMixin

from pages.models.about import AboutPartner, About, AboutStaff


class AboutPartnerInline(SortableInlineAdminMixin, TabularInline):
    model = AboutPartner
    fields = ('partner', 'order')
    extra = 0


class AboutStaffInline(SortableInlineAdminMixin, TabularInline):
    model = AboutStaff
    fields = ('person', 'order')
    extra = 0


class AboutAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.js',
            'theme/js/tinymce_ng.js'
        )
        css = {
            'all': (
                )
        }

    list_display = ('name',)

    inlines = [AboutPartnerInline, AboutStaffInline]

    fieldsets = (
        ('Title', {
            'fields': ('name', )
        }),
        ('Mission', {
            'fields': ('mission', )
        }),
        ('Team', {
            'fields': ('team',)
        }),
        ('Partners', {
            'fields': ('partners', )
        }),
        ('Funders', {
            'fields': ('funders', )
        }),
        ('Funders List', {
            'fields': ('funders_list', )
        }),
        ('Blurbs', {
            'fields': ('tagline', 'donate_message', 'jobs_message',)
            }
        ),
    )

admin.site.register(About, AboutAdmin)
