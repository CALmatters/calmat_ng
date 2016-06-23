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
from django.conf.urls import url
from pages.views import article_list, article_view, homepage_view, about_view

urlpatterns = [
    url('category/(?P<category>.*)/$',
        article_list,
        name='article_list_category'),

    url('^(?P<custom_post_type>.*)/all$',
        article_list,
        name='article_list_custom_post_type'),

    url('article/(?P<slug>[a-zA-Z0-9_-]+)/$',
        article_view,
        name='article_detail'),

    url('homepage/preview/(?P<homepage_id>\d+)/$',
        homepage_view,
        name='home_page_preview'),

    url('about/$', about_view, name='about_view'),

    url('$', article_list, name='article_list'),
]
