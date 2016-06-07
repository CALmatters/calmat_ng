from django import forms
from django.contrib import admin
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from business.models.authors import Author
from media_manager.widgets import PopupSelect
from sites.mixins.admin_thumb import AdminThumbMixin


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        widgets = {
            'image': PopupSelect(),
        }
        exclude = ()


class AuthorAdmin(AdminThumbMixin, admin.ModelAdmin):

    form = AuthorAdminForm

    list_display = [
        'admin_thumb_reference', 'username', 'first_name', 'last_name', 'user', 'email']
    list_display_links = ('username', 'first_name','last_name')

    readonly_fields = ('email', 'slug', 'full_name')
    fieldsets = (
        ('General', {
            'fields': (
                'status',
                'full_name',
                'email',
                'user')}),
        ('Profile Image',
         {'fields': (
             'job_title',
             'image',
             'twitter',
             'facebook_url')}),
    )

    admin_thumb_ref = 'image'
    admin_thumb_field = 'file'


admin.site.register(Author, AuthorAdmin)
