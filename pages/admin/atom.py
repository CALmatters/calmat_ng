from copy import copy

from django.contrib import admin


from pages.models import Atom


# Todo:  Generalize clone completely
from sites.mixins.admin_thumb import AdminThumbMixin


def duplicate_atom(modeladmin, request, queryset):
    """
    Add duplication as a dropdown option on admin page listing objets.

    http://blogs.law.harvard.edu/rprasad/2012/08/24/using-django-admin-to-copy-an-object/
    http://stackoverflow.com/questions/3989894/create-a-django-admin-action-to-duplicate-a-record#4054256
    """
    # atom is an instance of BlogAtom
    for atom in queryset:
        a_copy = copy(atom)  # django copy object
        a_copy.id = None   # set `id` to None to create new object
        a_copy.title = '{0} -- Copy'.format(a_copy.title)
        a_copy.created = None
        a_copy.updated = None
        a_copy.slug = None
        a_copy.publish_date = None
        a_copy.save()      # initial save

        # copy M2M relationship: categories
        for categories in atom.categories.all():
            a_copy.categories.add(categories)

        #  Todo:  This M2M?
        # # copy M2M relationship: related_persons
        # for related in atom.related.all():
        #     # add related as through model
        #     # https://docs.djangoproject.com/en/1.6/topics/db/models/
        #     # -- see #extra-fields-on-many-to-many-relationships
        #     through = BlogAtomRelatedAtomMeta(related_atom=a_copy, main_atom=related)
        #     through.save()

        a_copy.save()  # save the copy to the database for M2M relations

duplicate_atom.short_description = "Duplicate Atom"


class AtomAdmin(AdminThumbMixin, admin.ModelAdmin):
    # inlines = (RelatedAtomsInline,)

    # Todo:  Move to Admin super class parallel with ContentContainer is Sites
    class Media:
        js = (
            'https://cdn.tinymce.com/4/tinymce.min.js',
            'theme/js/tinymce_ng.js'
        )
        css = {
            'all': (
                )
        }

    actions = [duplicate_atom]
    list_display = (
        'title',
        'headline',
        'status',
        'publish_date',
        'default_display_type',
        'admin_thumb',
        # 'admin_link',
    )
    list_editable = ('status', 'default_display_type',)

    fieldsets = (
        ('Content', {"fields": (
            "title",
            "headline",
            "featured_image",
            "content",
            "embedded_content",
            "categories",
        )}),
        ('Options', {'fields': (
            'default_display_type',
            'modal_layout',
            'modal_layout_right',
        )}),
        ('Meta', {'fields': (
            'status',
            'publish_date',
            'description',
        )}),
    )

    admin_thumb_field = 'featured_image'

    filter_horizontal = ('categories',)
    # filters in right column
    list_filter = ("categories",)
admin.site.register(Atom, AtomAdmin)
