from django.conf.urls import url

from business.views import subscribe

urlpatterns = [
    url('subscribe/$',
        subscribe,
        name='subscribe'),
]
