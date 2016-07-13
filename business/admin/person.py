from django import forms
from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from business.models import Person
from media_manager.widgets import PopupSelect
from sites.mixins.admin_thumb import AdminThumbMixin


class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        widgets = {
            'image': PopupSelect(),
        }
        exclude = ()


class PersonAdmin(SortableAdminMixin, AdminThumbMixin, admin.ModelAdmin):

    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.min.js',
            'theme/js/tinymce_ng_specific_text_areas.js'
        )
        css = {
            'all': (
                )
        }

    form = PersonAdminForm

    list_display = [
        'admin_thumb_reference',
        'username',
        'first_name',
        'last_name',
        'user',
        'email',
        'staff_member',
        'director_board_member',
        'advisory_board',
    ]
    list_display_links = ('username', 'first_name','last_name')
    list_editable = ['staff_member', 'director_board_member', 'advisory_board',]

    readonly_fields = ('full_name',)
    fieldsets = (
        ('Idenfication', {
            'fields': (
                'user',
                'first_name',
                'last_name',
                'email',
                'full_name',
                'slug',
            )}),
        ('Details', {
            'fields': (
                'job_title',
                'image',
                'staff_member',
                'director_board_member',
                'advisory_board',
                'exerpt',
            )}),
        ('Content', {
            'fields': (
                'content',
            ),
            'classes': (
                "tinymce-editable",
            )
        }),
        ('Social',
         {'fields': (
             'twitter',
             'facebook_url')}),
    )

    admin_thumb_ref = 'image'
    admin_thumb_field = 'file'


admin.site.register(Person, PersonAdmin)
