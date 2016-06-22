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

    readonly_fields = ('email', 'slug', 'full_name',)
    fieldsets = (
        ('General', {
            'fields': (
                'user',
                'full_name',
                'job_title',
                'image',
                'email',
                'staff_member',
                'director_board_member',
                'advisory_board',
            )}),
        ('Social',
         {'fields': (
             'twitter',
             'facebook_url')}),
    )

    admin_thumb_ref = 'image'
    admin_thumb_field = 'file'


admin.site.register(Person, PersonAdmin)
