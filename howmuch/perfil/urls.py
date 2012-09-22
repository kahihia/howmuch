from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.perfil.views',
		url(r'^edit/$', 'edit' , name = "profileEdit"),
) 