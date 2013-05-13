from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.search.views',
        url(r'^$','searchservice', name = "searchservice"),
        url(r'^(?P<query>[a-zA-Z0-9_+-]+)/(?P<filters>[a-zA-Z0-9_+-]+)/$','search', name='search query'),
) 