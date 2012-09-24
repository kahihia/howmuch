from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.core.views',
		url(r'^item/new/$', 'requestItem' , name = "coreNewItem"),
		url(r'^proffer/new/(?P<itemId>\d+)/$', 'newProffer', name = "coreNewProffer"),
		url(r'^$','home', name = "coreHome"),
) 