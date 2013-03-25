from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.pays.views',

	    url(r'^test/$', 'paypal', name = 'test paypal'),
)