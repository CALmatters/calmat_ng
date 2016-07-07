"""calmat_ng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from calmat_ng.feeds import RssArticleFeed, AtomArticleFeed
from calmat_ng.views import search
from pages.views import (homepage_view, columns, columns_single, project_view,
                         article_list)

urlpatterns = [

    url(r'^admin_tools/', include('admin_tools.urls')),
    url("^$", homepage_view, name="home"),
    url(r'^admin/', admin.site.urls),
    url("^pages/", include("pages.urls"), name="pages"),
    url("^projects/$",
        project_view,
        name="projects"),
    url("^project/(?P<slug>[a-zA-Z0-9\-\_]+)/$",
        project_view,
        name="project_detail"),
    url("^atom/(?P<atom>.*)$",
        article_list,
        name="article_list_atom"),
    # url("^atom/(?P<slug>[A-Za-z0-9\-\_]+)$",
    #     "mezzcms.blog.views.atom_post_detail",
    #     name="atom_post_single"),

    url("^partner/(?P<partner>.*)$",
        article_list,
        name="article_list_partner"),

    url('^feeds/rss$', RssArticleFeed(), name='rss_article_feed'),
    url('^feeds/atom', AtomArticleFeed(), name='atom_article_feed'),
    url("^politics/$", columns, name="columns_list"),
    url("^politics/(?P<slug>[a-zA-Z0-9\-\_]+)/$",
        columns_single,
        name="columns_single"),
    url("^search/$", search, name="search"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

