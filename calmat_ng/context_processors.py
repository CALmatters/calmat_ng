from categories.models import Category

from pages.models import Project


def categories(request):
    data = dict(
        categories=Category.get_display_categories(),
        category_menus=Category.objects.filter(as_menu=True))
    return data


def projects(request):
    return dict(projects=Project.get_display_projects(request))
