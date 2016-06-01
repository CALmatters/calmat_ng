class AdminThumbMixin(object):
    """Provides a 50x50 thumbnail for VersitalImageFields.

    Put 'admin_thumb' in the list_display for and admin class, then
    add a attribute to the class named admin_thumb_field as set equal to
    a the string name of the image field on the model

    e.g.  admin_thumb_field = 'featured_image'

    assuming obj.feature_image exists.
    """

    admin_thumb_field = None

    def admin_thumb(self, obj):
        thumb = ""
        if self.admin_thumb_field:
            thumb = getattr(obj, self.admin_thumb_field, "")
        if not thumb:
            return ""
        return '<img src="{}" />'.format(thumb.thumbnail['50x50'].url)
    admin_thumb.allow_tags = True
    admin_thumb.short_description = "Featured Image"
