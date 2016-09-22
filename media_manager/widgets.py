from django.forms.widgets import Select

from django.template.loader import get_template
from django.utils.safestring import mark_safe

from media_manager.models import MediaItem


class PopupSelect(Select):

    class Media:
        js = ('popup_image_chooser_launcher.js', )

    def render(self, name, value, attrs=None, choices=()):
        elements = super(PopupSelect, self).render(name, value, attrs, choices)

        template = get_template('image_field.html')

        #  TODO:  DRY out, should be able to pull any object up, or better yet
        #  shouldn't need a DB hit
        try:
            media_obj = MediaItem.objects.get(pk=value)
        except MediaItem.DoesNotExist:
            media_obj = None

        controls = mark_safe(template.render(
            dict(title="Profile Image", media_obj=media_obj, field_name=name)))

        return mark_safe("{}  {}".format(elements, controls))


