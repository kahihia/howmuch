from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.Profile.views',
        url(r'^edit/$', 'edit' , name = "profileEdit"),
) 