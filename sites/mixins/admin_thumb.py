from django.utils.safestring import mark_safe

class AdminThumbMixin(object):
    """Provides a 50x50 thumbnail for VersitalImageFields.

    Put 'admin_thumb' in the list_display for and admin class, then
    add a attribute to the class named admin_thumb_field as set equal to
    a the string name of the image field on the model

    e.g.  admin_thumb_field = 'featured_image'

    assuming obj.feature_image exists.
    """

    admin_thumb_field = None
    admin_thumb_ref = None

    def admin_thumb(self, obj):
        thumb = ""
        if self.admin_thumb_field:
            thumb = getattr(obj, self.admin_thumb_field, "")
        if not thumb:
            return ""
        try:
            return '<img src="{}" />'.format(thumb.thumbnail['50x50'].url)
        except OSError:
            return ""
    admin_thumb.allow_tags = True
    admin_thumb.short_description = "Featured Image"

    def admin_thumb_reference(self, obj):
        thumb_ref = getattr(obj, self.admin_thumb_ref, "")
        thumb = getattr(thumb_ref, self.admin_thumb_field, "")
        if not thumb:
            return ""
        try:
            return mark_safe(
                '<img src="{}" />'.format(thumb.thumbnail['50x50'].url))
        except OSError:
            return ""

    admin_thumb_reference.allow_tags = True
    admin_thumb_reference.short_description = "Featured Image"
