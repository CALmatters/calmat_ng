from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from media_manager.models import MediaItem, MediaSource
from sites.mixins.admin_thumb import AdminThumbMixin


def _fb_file_link(obj):
    """Produce a link to start off the image placement when popping up

    See popup_<ver>.js for this buttons click event
    """

    fb_link = ('<button data-media-upload-url="/static/media/%s">'
               'Select</button>')
    return mark_safe(fb_link % obj.file)
_fb_file_link.short_description = "Select"


def _thumb_img(obj):
    """Return a thumbnail of obj.file.

    This gets the regular file, and scales  it down.

    Todo:  Is this the best way to do this?  If so, why do we have thumb images
    """

    thumb_element = ('<img style="width: 50px; height: 50px" '
                     'id="image_id_featured_image" '
                     'src="/static/media/%s" class="preview"></a>')
    return mark_safe(thumb_element % obj.file)


class MediaSourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(MediaSource, MediaSourceAdmin)


class MediaItemAdmin(AdminThumbMixin, admin.ModelAdmin):

    class Media:
        js = ("popup_v1.js",)

    adm_list_display = (
        'caption',
        'admin_thumb',
        'source',
        'creator',
        'image_type',
        'alt_tag',
        'license',
        'date')
    popup_list_display = (_fb_file_link, ) + adm_list_display
    adm_list_display_links = ('caption', )

    list_filter = ('source', 'creator', 'image_type', 'license')
    search_fields = (
        'caption',
        'source__title',
        'creator',
        'image_type',
        'alt_tag',
        'license',
        'file')

    admin_thumb_field = 'file'

    def get_list_display(self, request):
        """Conditionally display the images in a list in the change_list

        This is done conditionally to switch on and off the ability to set
        an image in content, or edit an image in the admin.  When specifying
        urls to launch this admin, add __admin__=1 to load the admin look, and
         __admin__=0 to load the popup look.

        """

        if request.GET.get('_popup', False):
            return MediaItemAdmin.popup_list_display
        else:
            return MediaItemAdmin.adm_list_display

    def get_list_display_links(self, request, list_display):
        if request.GET.get('_popup', False):
            return ()
        else:
            return MediaItemAdmin.adm_list_display_links

admin.site.register(MediaItem, MediaItemAdmin)
