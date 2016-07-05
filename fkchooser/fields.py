from django.db.models import ForeignKey
from django.forms import ModelChoiceField
from django.forms.widgets import Select

from django.template.loader import get_template
from django.utils.safestring import mark_safe


class PopupSelect(Select):

    url_filter = ''

    def render(self, name, value, attrs=None, choices=()):
        elements = super(PopupSelect, self).render(name, value, attrs, choices)

        template = get_template('fk_chooser_field.html')

        app = self.choices.queryset.model._meta.app_label
        model = self.choices.queryset.model._meta.model_name

        url = mark_safe("/admin/{}/{}/?_popup=1000&{}".format(
            app, model, self.url_filter))
        field_id = "id_{}".format(name)

        controls = mark_safe(template.render(dict(url=url, field_id=field_id)))
        return mark_safe("{}  {}".format(elements, controls))


def get_class(url_filter=None):

    if not url_filter:
        widget = PopupSelect
    else:
        select_attrs = dict(url_filter=url_filter)
        widget = type(
            'FilteredPopupSelect_{}'.format(len(url_filter)),
            (PopupSelect,), select_attrs)

    attrs = dict(widget=widget)
    return type(
        'FilteredPopupModelChoiceField_{}'.format(widget.__class__),
        (ModelChoiceField,), attrs)


class PopupForeignKey(ForeignKey):
    """"Subclass of the Model Field"""

    def __init__(self, to, url_filter='', on_delete=None,
                 related_name=None, related_query_name=None,
                 limit_choices_to=None, parent_link=False, to_field=None,
                 db_constraint=True, **kwargs):

        #  Save a specific url filter string for this FK instance
        self.url_filter = url_filter

        super(PopupForeignKey, self).__init__(
            to, on_delete, related_name, related_query_name, limit_choices_to,
            parent_link, to_field, db_constraint, **kwargs)

    def formfield(self, **kwargs):
        """Return a PopupModelChoiceField Form Field"""

        #  Create a ModelChoiceField subclass class setting to set filter
        form_class = get_class(self.url_filter)

        defaults = dict(form_class=form_class)
        defaults.update(kwargs)

        return super(PopupForeignKey, self).formfield(**defaults)



