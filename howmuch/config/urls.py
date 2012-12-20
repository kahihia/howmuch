from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.config.views',
        url(r'^notifications/$', 'edit_config' , name = "configEditConfig"),        
) 