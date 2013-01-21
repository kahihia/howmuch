from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.home.views',
        url(r'^$','home', name = "homepage"),
) 