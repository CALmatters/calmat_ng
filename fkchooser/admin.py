from django.contrib import admin
from django.utils.safestring import mark_safe


class FKChooserAdminMixin(admin.ModelAdmin):

    def _fb_file_link(self, obj):
        fb_link = mark_safe(
            '<button data-fk-id="{}">Select</button>'.format(obj.id))
        return fb_link
    _fb_file_link.short_description = "Select"

    def get_list_display(self, request):
        list_display = super(
                FKChooserAdminMixin, self).get_list_display(request)
        if request.GET.get('_popup', False):
            list_display = ['_fb_file_link', ] + list(list_display)
        return list_display

    def get_list_display_links(self, request, list_display):

        if request.GET.get('_popup', False):
            return ()
        else:
            return super(
                FKChooserAdminMixin, self).get_list_display_links(
                request, list_display)

    def changelist_view(self, request, extra_context=None):

        template_response = super(FKChooserAdminMixin, self).changelist_view(
            request, extra_context)

        #  if this request leads to a popup (really should be our popup)
        #  add the popup controller codd to the response media
        if request.GET.get('_popup', False):
            template_response.context_data['media']._js.append(
                'fk_static_files/popup_fk_controller.js')

        return template_response
