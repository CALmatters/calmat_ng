from categories.models import Category

# Todo:  move these to the apps they reference
from pages.models import Project


def categories(request):
    return dict(categories=Category.get_display_categories())


def projects(request):
    return dict(projects=Project.get_display_projects(request))
