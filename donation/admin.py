from django.contrib import admin

from .models import *

#-------------------------------------------------------------------------------
#   :: Donate page
#-------------------------------------------------------------------------------

class DonateAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.js',
            'theme/js/tinymce_ng.js'
        )
        css = {
            'all': (
                )
        }

    list_display = ('name',)
    fieldsets = (
        ('Page Title', {
            'fields': ('name',)
            }
        ),
        ('Orange Box Content', {
            'fields': ('donate_message','donate_message_image',)
            }
        ),
        ('Donation Section', {
            'fields': ('donate_section_top', 'donate_section_bottom',)
            }
        ),
        ('Tell Section', {
            'fields': ('tell_section',)
            }
        ),
    )
admin.site.register(Donate, DonateAdmin)

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