from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from categories.models import Category


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):

    list_display = ("title", "slug")

    readonly_fields = ("slug", )
    fieldsets = ((None,
                  {"fields": (
                      "title", "slug")}),)

admin.site.register(Category, CategoryAdmin)
