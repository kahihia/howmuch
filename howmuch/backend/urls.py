# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.backend.views',
		url(r'^inboxcount/$', 'inboxCount', name = "backendInboxCountView"),
		url(r'^notificationscount/$', 'notificationsCount', name = "backendNotificationsCountView")
) 