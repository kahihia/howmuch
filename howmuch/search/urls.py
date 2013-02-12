from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.search.views',
        url(r'^$','searchservice', name = "searchservice"),

) 