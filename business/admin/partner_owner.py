from django.contrib import admin

from business.models import PartnerOwner


class PartnerOwnerAdmin(admin.ModelAdmin):

    list_display = ('title', )
    fieldsets = (
        (None, {
            'fields': ('title', )
        }),
    )

admin.site.register(PartnerOwner, PartnerOwnerAdmin)

