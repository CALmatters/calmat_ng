class AdminCatListMixin(object):
    """List out the obj.categories for list_displays"""

    def category_list(self, obj):

        return ", ".join([c.title for c in obj.categories.all()])

    category_list.allow_tags = True
    category_list.short_description = "Categories"
