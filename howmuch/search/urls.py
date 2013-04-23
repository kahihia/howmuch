from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.search.views',
        url(r'^$','searchservice', name = "searchservice"),
        url(r'^(?P<query>[a-zA-Z0-9+-]+)/$','search_query', name='search query'),
        url(r'^_(?P<filters>[a-zA-Z0-9_+-]+)$','search_filters', name='search filters'),
        url(r'^(?P<query>[a-zA-Z0-9+-]*)_(?P<filters>[a-zA-Z0-9_+-]+)$','search_query_filters', name='search query filters'),
) 