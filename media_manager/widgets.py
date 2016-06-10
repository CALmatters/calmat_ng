from django.forms.widgets import Select

from django.template.loader import get_template
from django.utils.safestring import mark_safe


class PopupSelect(Select):

    class Media:
        js = ('popup_launcher.js', )

    def render(self, name, value, attrs=None, choices=()):
        elements = super(PopupSelect, self).render(name, value, attrs, choices)

        template = get_template('image_field.html')

        controls = mark_safe(template.render(
            dict(title="Profile Image", media_obj=value)))

        return mark_safe("{}  {}".format(elements, controls))


