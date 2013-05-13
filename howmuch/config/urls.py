from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change

from howmuch.settings import CHANGE_CONFIG_REDIRECT

urlpatterns = patterns('howmuch.config.views',
        url(r'^notifications/$', 'notifications_config' , name="edit config"), 
        url(r'^password/$', password_change, {'post_change_redirect' : CHANGE_CONFIG_REDIRECT }),
        url(r'^email/$', 'change_email', name='change email'),       
) 