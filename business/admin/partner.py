from django.contrib import admin

from business.models import Partner


class PartnerAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.min.js',
            'theme/js/tinymce_ng.js'
        )
        css = {
            'all': (
            )
        }

    list_display = (
        'title',
        'partner_type',
        'link_to_articles',
        'partner_owner')

    fieldsets = (
        ("Title", {
            "fields": (
                "title",
                "owner",
                "partner_type",
                "link_to_articles")
        }),
        ("Featured Image", {
            "fields": (
                "featured_image",
                "featured_image_large")
        }),
        ("Categories", {
            "fields": (
                "categories", )
        }),
    )
    filter_horizontal = ('categories',)

    # filters in right column
    list_filter = ("categories", "partner_type", "owner")

admin.site.register(Partner, PartnerAdmin)
