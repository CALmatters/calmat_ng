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
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView, TemplateView

from business.views import subscribe
from calmat_ng.feeds import RssArticleFeed, AtomArticleFeed
from calmat_ng.sitemaps import NewsSitemap
from calmat_ng.views import search
from employment.views import jobs_view, jobs_listing_view
from media_manager.views import media_lookup
from pages.views import (homepage_view, columns, columns_single, project_view,
                         article_list, article_view, about_view, team_list,
                         about_partners_list, atom_detail, contact_us,
                         proposition_view, proposition_list)
from donation.views import DonatePageView, StripeCustomerView

urlpatterns = [

    url(r'^admin_tools/', include('admin_tools.urls')),
    url("^$", homepage_view, name="home"),

    url(r'^admin/', admin.site.urls),

    url("^articles/(?P<slug>proposition-[a-zA-Z0-9\-\_]+)/",
        RedirectView.as_view(pattern_name='proposition_detail')),

    url('articles/(?P<slug>[a-zA-Z0-9_-]+)/$',
        article_view,
        name='article_detail'),
    url('^articles/(?P<custom_post_type>.*)/all$',
        article_list,
        name='article_list_custom_post_type'),

    url('homepage/preview/(?P<homepage_id>\d+)/$',
        homepage_view,
        name='home_page_preview'),

    url('about/$', about_view, name='about_view'),
    url('about/partners/$', about_partners_list, name='about_view'),
    url('about/(?P<team_filter>[a-zA-Z0-9\-\_]+)/(?P<individual>[a-zA-Z0-9\-\_]+)/$',
        team_list,
        name='about_team'),
    url('about/(?P<team_filter>[a-zA-Z0-9\-\_]+)/$',
        team_list,
        name='about_individual'),

    url('jobs/?$', jobs_view, name='job_view'),
    url('job/(?P<slug>[a-zA-Z0-9\-\_]+)/?$', jobs_listing_view, name='job_view'),

    url('category/(?P<category>.*)/$',
        article_list,
        name='article_list_category'),

    # url("^pages/", include("pages.urls"), name="pages"),

    url("^projects/$",
        project_view,
        name="projects"),

    url("^project/(?P<slug>[a-zA-Z0-9\-\_]+)/$",
        project_view,
        name="project_detail"),

    url("^proposition/(?P<slug>[a-zA-Z0-9\-\_]+)/$",
        proposition_view,
        name="proposition_detail"),

    #  People will get to it by going to calmatters.org/elections
    #  (the shortcode we discussed), or navigating to it from the
    # Propositions 2016 item in the menu.
    url('^elections/(?P<voter_guide_slug>[a-zA-Z0-9\-\_]*)/$',
        proposition_list,
        name='voter_guide'),
    url('^elections/$',
        proposition_list,
        name='voter_guide'),
    url('^propositions/$',
        proposition_list,
        name='proposition_list'),
    url('^propositions/(?P<category_slug>[a-zA-Z0-9\-\_]*)/$',
        proposition_list,
        name='proposition_list'),

    url("^atom/(?P<slug>[A-Za-z0-9\-\_]+)$",
        atom_detail,
        name="atom_detail"),
    url("^atom/(?P<atom>.*)$",
        article_list,
        name="article_list_atom"),

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
    url("^donate/$", DonatePageView, name="donate"),
    url("^donation/(?P<amount>[a-zA-Z0-9\-\_]+)/$", StripeCustomerView.as_view(), name="donate_amount"),
    url("^donation/$", StripeCustomerView.as_view(), name="donate_form"),

    #  Redirects for existing urls
    url("^stories/$", RedirectView.as_view(pattern_name='projects')),
    url("^stories/(?P<slug>[a-zA-Z0-9\-\_]+)/$",
        RedirectView.as_view(pattern_name='project_detail')),
    url("^newsanalysis/$", RedirectView.as_view(pattern_name='columns_list')),
    url("^newsanalysis/(?P<slug>[a-zA-Z0-9\-\_]+)/$",
        RedirectView.as_view(pattern_name='columns_single')),


    url('subscribe/$', subscribe, name='subscribe'),
    url('contact_us/$', contact_us, name='contact_us'),
    url('privacy-policy/$',
        TemplateView.as_view(template_name="privacy_policy.html")),
    url('terms-conditions/$',
        TemplateView.as_view(template_name="terms_conditions.html")),

    # url(r'^sitemap\.xml$', sitemap, {'sitemaps': CALmattersSitemap},
    #     name='django.contrib.sitemaps.views.sitemap')

    url(r'^news-sitemap\.xml$', sitemap, {
        'sitemaps': {'news': NewsSitemap},
        'template_name': 'news_sitemap.xml'
    }),
    url(r'^media_lookup/(\d+)/$', media_lookup),

    url(r'^robots\.txt', include('robots.urls')),

    #  Alternate short url to projects.
    #  Must be at bottom to give all other possible matching
    #  TODO:  Consider someday the desire to shorten urls to articles
    url("^(?P<slug>[a-zA-Z0-9\-\_]+)/$", project_view),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

