from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.core.views',
		url(r'^item/new/$', 'requestItem' , name = "corenewitem"),
		url(r'^$','home', name = "corehome"),
) 