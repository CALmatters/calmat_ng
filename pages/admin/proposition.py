from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django import forms
from django.utils.timezone import now

from categories.mixins import AdminCatListMixin
from fkchooser.admin import FKChooserAdminMixin
from media_manager.widgets import PopupSelect
from pages.models import Atom

# Todo:  Generalize clone completely
from cmskit.mixins.admin_thumb import AdminThumbMixin
from pages.models.proposition import Proposition, VoterGuide, PoliticalEntity


class PoliticalEntityAdmin(AdminThumbMixin, admin.ModelAdmin):

    list_display = [
        "title",
        "admin_thumb_reference",
    ]

    admin_thumb_ref = "image"
    admin_thumb_field = 'file'

admin.site.register(PoliticalEntity, PoliticalEntityAdmin)


class PropositionInline(SortableInlineAdminMixin, admin.StackedInline):

    model = Proposition
    fields = ('title', 'order')
    min_num = 0
    extra = 0


class VoterGuideAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "can_go_live",
        "go_live_on_date",
        "current_live",
    ]
    readonly_fields = ('slug',)
    list_editable = ('can_go_live',)
    inlines = (PropositionInline, )

    fieldsets = (
        (None, {
            "fields": (
                "title",
                "can_go_live",
                "go_live_on_date",
            )
        }),)

    #  TODO:  move current live concept to supoer class/mixin, in homepage too
    def current_live(self, obj):
        try:
            live_obj = VoterGuide.objects.get_live_object()
        except IndexError:
            live_obj = None

        if not obj.can_go_live:
            return ""
        elif live_obj and obj == live_obj:
            return '** LIVE **'
        elif not obj.go_live_on_date or obj.go_live_on_date < now():
            return ""
        elif obj.go_live_on_date > now():
            dt = obj.go_live_on_date - now()
            return "{} days, {} hours, {} minutes TO LIVE".format(
                dt.days, int(dt.seconds / 3600), dt.seconds % 60)

    current_live.short_description = "Live Status"

admin.site.register(VoterGuide, VoterGuideAdmin)


class PropositionAdminForm(forms.ModelForm):
    class Meta:
        model = Atom
        widgets = {
            'image': PopupSelect(),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
        exclude = ()


class PropositionAdmin(AdminThumbMixin, AdminCatListMixin, FKChooserAdminMixin,
                       admin.ModelAdmin):

    form = PropositionAdminForm

    # Todo:  Move to Admin super class parallel with ContentContainer is Sites
    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.min.js',
            'theme/js/image_file_picker.js',
            'theme/js/tinymce_ng_specific_text_areas.js'
        )
        css = {
            'all': (
                )
        }

    list_display = (
        'title',
        'category_list',
        'voter_guide',
    )
    filter_horizontal = ('categories', 'supporters', 'opponents')
    list_filter = ("categories",)
    search_fields = ('title', 'content')

    fieldsets = (
        ('Content', {"fields": (
            "voter_guide",
            "title",
            "slug",
            "image",
            "categories",
            "supporters",
            "opponents",
        )}),
        ('Content', {
            'fields': (
                "content",
            ),
            'classes': (
                "tinymce-editable",
            )
        }),
        ('More information', {
            'fields': (
                "more_information",
            ),
            'classes': (
                "tinymce-editable",
            )
        }),
    )

    admin_thumb_ref = "image"
    admin_thumb_field = 'file'

admin.site.register(Proposition, PropositionAdmin)
