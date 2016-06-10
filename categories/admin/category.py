from django.contrib import admin

from categories.models import Category


class CategoryAdmin(admin.ModelAdmin):

    list_display = ("title", "slug")

    readonly_fields = ("slug", )
    fieldsets = ((None,
                  {"fields": (
                      "title", "slug")}),)

admin.site.register(Category, CategoryAdmin)
