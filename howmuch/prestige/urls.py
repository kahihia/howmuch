from django.conf.urls import patterns, include, url


urlpatterns = patterns('howmuch.prestige.views',
		url(r'^critiques/(?P<username>\w+)/$', 'critiques', name="critiques"),
        url(r'^confirmpay/(?P<assignmentID>\d+)/$', 'confirm_pay', name="confirm_pay"),
        url(r'^confirmdelivery/(?P<assignmentID>\d+)/$', 'confirm_delivery', name="confirm_delivery"),
        url(r'^critique/(?P<assignmentID>\d+)/$', 'critique', name="critique"),
) 