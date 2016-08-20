class AdminCatListMixin(object):
    """List out the obj.categories for list_displays"""

    def category_list(self, obj):

        return ", ".join([c.title for c in obj.categories.all()])

    category_list.allow_tags = True
    category_list.short_description = "Categories"


class CategoryMixin(object):
    # Intended to be mixed with a model.
    # The module must have a categories field.

    def get_category_ids(self, preferred_only=True):
        """
        Return a list of category IDs
        """

        if not preferred_only:
            cats = self.categories.all()
        else:
            cats = self.categories.filter(preferred=True)

        cat_ids = [c.id for c in cats]
        if cat_ids:
            return cat_ids
