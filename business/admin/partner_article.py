from django.contrib import admin

from business.models.partner_article import PartnerArticle


class PartnerArticleAdmin(admin.ModelAdmin):

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

    list_filter = ('partner__owner', 'partner', )
    readonly_fields = ('order', )

    def partner_owner(self, obj):
        return obj.partner.partner_owner()

    def note_first_chars(self, obj):

        if obj.notes and len(obj.notes) > 100:
            return "%s ..." % obj.notes[:100]
        else:
            return obj.notes
    note_first_chars.short_description = 'Notes'


admin.site.register(PartnerArticle, PartnerArticleAdmin)
