from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.messages.views',
	
        url(r'^(?P<conversationID>\d+)/$', 'postMessage' , name = "post message"),
        url(r'^inbox/$', 'inbox' , name = "inbox"),     

        url(r'^infobuyer/(?P<conversationID>\d+)/$', 'getInfoBuyer', name = 'getInfoBuyer'),
        url(r'^infoseller/(?P<conversationID>\d+)/$', 'getInfoSeller', name = 'getInfoSeller'),
        url(r'^infoconfirmpay/(?P<conversationID>\d+)/$', 'getInfoConfirmPay', name = 'getInfoConfirmPay'),
        url(r'^infoconfirmdelivery/(?P<conversationID>\d+)/$', 'getInfoConfirmDelivery', name = 'getInfoConfirmDelivery'),
        url(r'^infocritique/(?P<conversationID>\d+)/$', 'getInfoCritique', name = 'getInfoCritique')
) 