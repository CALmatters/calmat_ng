from copy import copy

from cmskit.models import Named, TimeStamped
from cmskit.models.publishable import CONTENT_STATUS_DRAFT, Publishable
from pages.models import HomePage


class Cloneable(object):
    """Copy and save all the fields and m2m records

    Sets a Duplicate choice in the action menu
    """

    def clone(self, request, queryset):

        for obj in queryset:
            if not obj.pk:
                raise ValueError(
                    'Instance must be saved before it can be cloned.  %s' % obj)

            new_object = copy(obj)
            new_object.id = new_object.pk = None

            # Todo:  Move this to Named.clone
            if isinstance(obj, Named):
                new_object.title = "{} copy".format(obj.title)
                new_object.slug = None

            #  Generalize these fields to a cmskit
            if isinstance(obj, HomePage):
                new_object.can_go_live = False
                new_object.go_live_on_date = None

            # Todo:  Move this to TimeStamped.clone
            if isinstance(obj, TimeStamped):
                new_object.created = None
                new_object.updated = None

            # Todo:  Move this to Publishable.clone
            if isinstance(obj, Publishable):
                new_object.status = CONTENT_STATUS_DRAFT
                new_object.publish_date = None

            new_object.save()

            for rel_model in obj._meta.many_to_many:
                for rel_obj in rel_model.rel.through.objects.filter(
                        **{str(obj._meta.model_name): obj}):
                    new_rel_obj = copy(rel_obj)
                    new_rel_obj.id = new_rel_obj.pk = None
                    setattr(new_rel_obj, obj._meta.model_name, new_object)
                    new_rel_obj.save()


            #  TODO:  Handle inlines

    def get_actions(self, request):
        """Overridden to add Clone to the actions

        From Django:  The keys are action names, and the values are
        (function, name, short_description) tuples.
        """

        actions = super(Cloneable, self).get_actions(request)

        actions.update(dict(clone=(
            Cloneable.clone,
            'clone',
            'Duplicate selected %s ' % self.opts.model_name)))

        return actions
