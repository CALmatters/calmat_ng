from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from categories.models import Category


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):

    list_display = ("title", "slug", "preferred", "as_menu")

    list_editable = ("preferred", "as_menu")
    readonly_fields = ()
    fieldsets = ((None,
                  {"fields": (
                      "title",
                      "slug",
                      "preferred",
                      "as_menu")
                  }),)

admin.site.register(Category, CategoryAdmin)
