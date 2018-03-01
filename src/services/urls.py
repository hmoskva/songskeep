from django.conf.urls import url

from .views import SiteListView, SongListView, songs_archive, subscribe, fetch_ajax_sites_by_category


urlpatterns = [
    url(r'^$', SiteListView.as_view(), name='index'),
    url(r'^(?P<slug>[\w-]+)/$', SongListView.as_view(), name='songs'),
    url(r'^archive/(?P<slug>[\w-]+)/$', songs_archive, name='archive'),
    url(r'^subscribe', subscribe, name='subscribe'),
    url(r'^fetch_sites_by_cat_ajax', fetch_ajax_sites_by_category, name='fetch_by_cat')
]