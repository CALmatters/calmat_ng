from django.contrib import admin

from pages.models import OnRamp


class OnRampAdmin(admin.ModelAdmin):

    # Todo:  Move to Admin super class parallel with ContentContainer is Sites
    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.min.js',
            'theme/js/image_file_picker.js',
            'theme/js/tinymce_ng.js'
        )
        css = {
            'all': (
            )
        }

    list_display = (
        'title',
    )

    fieldsets = (
        ('Content', {"fields": (
            "title",
            "content",
            "custom_link",
        )}),
    )
admin.site.register(OnRamp, OnRampAdmin)
