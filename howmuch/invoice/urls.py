from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.invoice.views',

	    url(r'^$', 'invoice', name='invoice'),  

) 