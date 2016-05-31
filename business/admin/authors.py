from django.contrib import admin

from business.models.authors import Author


class AuthorAdmin(admin.ModelAdmin):

    list_display = ['username', 'first_name', 'last_name', 'user', 'email']
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
             'content',
             'job_title',
             'profile_image',
             'twitter',
             'facebook_url')}),
    )
admin.site.register(Author, AuthorAdmin)
