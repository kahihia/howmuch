from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.notifications.views',
        url(r'^$', 'viewNotifications' , name = "viewNotifications"),   
) 