from django.contrib import admin

from pages.models.contact_us import ContactUs


class ContactUsAdmin(admin.ModelAdmin):

    list_display = ('first_name','last_name', 'email','about')

    fieldsets = (
        ('', {
            'fields': ('first_name', 'last_name', 'email', 'about', 'message')
        }),
    )

admin.site.register(ContactUs, ContactUsAdmin)
