from django import forms
from django.contrib import admin

from business.models import Partner
from media_manager.widgets import PopupSelect


class PartnerAdminForm(forms.ModelForm):
    class Meta:
        model = Partner
        widgets = {
            'image': PopupSelect(),
            'image_large': PopupSelect(),
        }
        exclude = ()


class PartnerAdmin(admin.ModelAdmin):

    form = PartnerAdminForm

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
        'partner_type',
        'link_to_articles',
        'partner_owner',
        'featured')

    list_editable = ("featured", )

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
                "image",
                "image_large")
        }),
        ("Categories", {
            "fields": (
                "categories", )
        }),
    )
    filter_horizontal = ('categories',)

    # filters in right column
    list_filter = ("categories", "featured", "partner_type", "owner")

admin.site.register(Partner, PartnerAdmin)
