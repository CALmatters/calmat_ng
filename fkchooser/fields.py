from django.conf import settings
from django.db.models import ForeignKey
from django.forms import ModelChoiceField
from django.forms.widgets import Select

from django.template.loader import get_template
from django.utils.safestring import mark_safe


class PopupSelect(Select):

    def render(self, name, value, attrs=None, choices=()):
        elements = super(PopupSelect, self).render(name, value, attrs, choices)

        template = get_template('fk_chooser_field.html')

        app = self.choices.queryset.model._meta.app_label
        model = self.choices.queryset.model._meta.model_name

        url = "/admin/{}/{}/?_popup=1000".format(app, model)
        field_id = "id_{}".format(name)

        controls = mark_safe(template.render(dict(url=url, field_id=field_id)))
        return mark_safe("{}  {}".format(elements, controls))


class PopupModelChoiceField(ModelChoiceField):
    """Subclass of Form Field"""

    widget = PopupSelect


class PopupForeignKey(ForeignKey):
    """"Subclass of the Model Field"""

    def formfield(self, **kwargs):
        """Return a PopupModelChoiceField Form Field"""

        defaults = dict(form_class=PopupModelChoiceField)
        defaults.update(kwargs)

        return super(PopupForeignKey, self).formfield(**defaults)



