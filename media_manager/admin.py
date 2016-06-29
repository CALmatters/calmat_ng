from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from media_manager.models import MediaItem, MediaSource
from sites.mixins.admin_thumb import AdminThumbMixin


def _fb_file_link(obj):
    """Produce a link to start off the image placement when popping up

    See popup_<ver>.js for this buttons click event
    """

    fb_link = mark_safe(
        '<button data-media-upload-id={} data-media-upload-url="{}">'
        'Select</button>'.format(obj.id, obj.file.url))
    return fb_link
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

    list_per_page = 20

    adm_list_display = (
        'caption',
        'admin_thumb',
        'source',
        'creator',
        'image_type',
        'alt_tag',
        'license',
        'date',)
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

    def image_preview(self, obj):
        return mark_safe('<img src="{}" />'.format(obj.file.url))
    image_preview.short_description = "Image Preview"

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return 'image_preview',
        else:
            return ()

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
