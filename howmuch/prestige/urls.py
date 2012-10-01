from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.prestige.views',
		url(r'^confirmpay/(?P<assignmentID>\d+)/$', 'confirmPay', name="prestigeConfirmPay"),
		url(r'^confirmdelivery/(?P<assignmentID>\d+)/$', 'confirmDelivery', name="prestigeConfirmDelivery"),
		url(r'^setprestigesaller/(?P<assignmentID>\d+)/$', 'setPrestigeSaller', name="prestigeSetPrestigeSaller"),
		url(r'^setprestigebuyer/(?P<assignmentID>\d+)/$', 'setPrestigeBuyer', name="prestigeSetPrestigeBuyer"),
) 