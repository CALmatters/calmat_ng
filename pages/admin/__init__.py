from django.conf import settings
from django.contrib import admin

from .article import ArticleAdmin
from .homepage import HomePageAdmin
from .atom import AtomAdmin
from .project import ProjectAdmin
from .onramp import OnRampAdmin
from .quote import QuoteAdmin
from .about import AboutAdmin
from .contact_us import ContactUsAdmin
from .proposition import PropositionAdmin

admin.site.site_header = u"{} Administration".format(settings.PROJECT_NAME)
# admin.site.disable_action('delete_selected')
