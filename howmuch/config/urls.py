from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change

urlpatterns = patterns('howmuch.config.views',
        url(r'^notifications/$', 'notifications_config' , name = "edit config"), 
        url(r'^password/$', password_change),
        url(r'^email/$', 'change_email', name='change email'),       
) 