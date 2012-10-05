from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.searchengine.views',
		url(r'^indexsearch/$','indexsearch', name = "indexsearch"),
		url(r'^$','searchservice', name = "searchservice"),

) 