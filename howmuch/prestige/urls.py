from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.prestige.views',
		url(r'^confirmpay/(?P<assignmentID>\d+)/$', 'confirmPay', name="prestigeConfirmPay"),
		url(r'^confirmdelivery/(?P<assignmentID>\d+)/$', 'confirmDelivery', name="prestigeConfirmDelivery"),
		url(r'^setprestigetoseller/(?P<assignmentID>\d+)/$', 'setPrestigeToSeller', name="prestigeSetPrestigeToSeller"),
		url(r'^setprestigetobuyer/(?P<assignmentID>\d+)/$', 'setPrestigeToBuyer', name="prestigeSetPrestigeToBuyer"),
) 