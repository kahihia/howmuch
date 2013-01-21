from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.config.views',
        url(r'^notifications/$', 'notifications_config' , name = "configEditConfig"),        
) 