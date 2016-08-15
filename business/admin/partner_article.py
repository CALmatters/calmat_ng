from django.contrib import admin

from business.models.partner_article import PartnerArticle
from cmskit.mixins.exportable import AdminCSVExport


class PartnerArticleAdmin(AdminCSVExport, admin.ModelAdmin):

    list_display = (
        'article',
        'partner',
        'partner_owner',
        'date_published',
        'print_publish',
        'radio_broadcast',
        'properly_credited',
        'fulltext_or_mention',
        'note_first_chars')

    list_filter = ('partner__owner', 'partner', 'radio_broadcast')
    readonly_fields = ('order', )

    search_fields = ("article__title", 'partner__title', )

    def partner_owner(self, obj):
        return obj.partner.partner_owner()

    def note_first_chars(self, obj):

        if obj.notes and len(obj.notes) > 100:
            return "%s ..." % obj.notes[:100]
        else:
            return obj.notes
    note_first_chars.short_description = 'Notes'

admin.site.register(PartnerArticle, PartnerArticleAdmin)
