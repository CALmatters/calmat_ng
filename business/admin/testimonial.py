from django import forms
from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from business.models import Testimonial
from media_manager.widgets import PopupSelect
from sites.mixins.admin_thumb import AdminThumbMixin


class TestimonialAdmin(SortableAdminMixin, AdminThumbMixin, admin.ModelAdmin):

    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.js',
            'theme/js/tinymce_ng.js'
        )
        css = {
            'all': (
                )
        }

    list_display = [
       'admin_thumb_reference', 'full_name', 'job_title', 'status',
    ]
    list_display_links = ('admin_thumb_reference', 'full_name',)

    fieldsets = (
        ('Testimonial', {
            'fields': ('full_name', 'job_title', 'message', 'testimonial_image',)
        }),
        ('Publishing', {
            'fields': ('status', 'publish_date',)    
        }),
    )

    admin_thumb_ref = 'testimonial_image'
    admin_thumb_field = 'file'

admin.site.register(Testimonial, TestimonialAdmin)
