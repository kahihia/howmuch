from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.invoice.views',

	    url(r'^$', 'invoice', name='invoice'),  
	    url(r'^pay/(?P<invoiceID>\d+)/$', 'pay', name='pay invoice'),
) 