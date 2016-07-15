from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.admin import TabularInline

from employment.models import JobPage, RelatedJobListings, JobListing


class RelatedJobListingsInline(SortableInlineAdminMixin, TabularInline):
    model = RelatedJobListings
    fields = ('job_listing', 'order')
    max_num = 100
    extra = 0


class JobPageAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.js',
            'theme/js/tinymce_ng_specific_text_areas.js',
        )
        css = {
            'all': (
                )
        }

    list_display = ('title', 'created')

    fieldsets = (
        (None, {"fields": (
            "title",
        )}),
        ('Content', {
            'fields': (
                "content",
            ),
            'classes': (
                "tinymce-editable",
            )
        }),
    )

    inlines = (RelatedJobListingsInline, )

admin.site.register(JobPage, JobPageAdmin)


class JobListingAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.js',
            'theme/js/tinymce_ng_specific_text_areas.js',
        )
        css = {
            'all': (
                )
        }

    list_display = ('title', 'status')

    fieldsets = (
        (None, {"fields": (
            "title",
            "status",
            'description',
        )}),
        ('Content', {
            'fields': (
                "content",
            ),
            'classes': (
                "tinymce-editable",
            )
        }),
    )


admin.site.register(JobListing, JobListingAdmin)

