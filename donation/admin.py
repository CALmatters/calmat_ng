from django.contrib import admin

from .models import *


#-------------------------------------------------------------------------------
#   :: StripeCustomer (fullstack labs)
#-------------------------------------------------------------------------------

class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name','stripe_email','created',)
    readonly_fields = ('stripe_id','created')
    fieldsets = (
        ('Customer', {
            'fields': ('stripe_id','first_name', 'last_name','stripe_email','phone',)
            }
        ),
        ('Contact', {
            'fields': ('address1','address2','city','state','zip_code',)
            }
        ),
    )
admin.site.register(StripeCustomer, StripeCustomerAdmin)