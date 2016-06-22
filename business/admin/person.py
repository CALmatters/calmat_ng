from django import forms
from django.contrib import admin

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


class PersonAdmin(AdminThumbMixin, admin.ModelAdmin):

    form = PersonAdminForm

    list_display = [
        'admin_thumb_reference',
        'username',
        'first_name',
        'last_name',
        'user',
        'email']
    list_display_links = ('username', 'first_name','last_name')

    readonly_fields = ('email', 'slug', 'full_name')
    fieldsets = (
        ('General', {
            'fields': (
                'user',
                'full_name',
                'job_title',
                'image',
                'email'
            )}),
        ('Social',
         {'fields': (
             'twitter',
             'facebook_url')}),
    )

    admin_thumb_ref = 'image'
    admin_thumb_field = 'file'


admin.site.register(Person, PersonAdmin)
