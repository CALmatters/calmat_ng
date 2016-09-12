from categories.models import Category

# Todo:  move these to the apps they reference
from pages.models import Project
from pages.models.proposition import VoterGuide


def categories(request):
    return dict(categories=Category.get_display_categories())


def projects(request):
    return dict(projects=Project.get_display_projects(request))


def live_voter_guide(request):
    return dict(live_voter_guide=VoterGuide.objects.get_live_object())
