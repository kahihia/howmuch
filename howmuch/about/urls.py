from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.about.views',

	    url(r'^privacy/$', 'privacy', name='privacy'),  
	    url(r'^terms/$', 'terms', name='terms'),
	    url(r'^faq/$', 'faq', name='faq')

) 