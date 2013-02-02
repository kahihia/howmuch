from django.conf.urls import patterns, include, url
from howmuch.messages.views import Conversation

urlpatterns = patterns('howmuch.messages.views',
	
        url(r'^(?P<conversationID>\d+)/$', 'view_conversation' , name = "post message"),
        url(r'^inbox/$', 'inbox' , name = "inbox"),   

        url(r'^send/(?P<conversationID>\d+)/$', 'send', name='sendmessage'),  

        url(r'^infobuyer/(?P<conversationID>\d+)/$', 'getInfoBuyer', name = 'getInfoBuyer'),
        url(r'^infoseller/(?P<conversationID>\d+)/$', 'getInfoSeller', name = 'getInfoSeller'),
        url(r'^infoconfirmpay/(?P<conversationID>\d+)/$', 'getInfoConfirmPay', name = 'getInfoConfirmPay'),
        url(r'^infoconfirmdelivery/(?P<conversationID>\d+)/$', 'getInfoConfirmDelivery', name = 'getInfoConfirmDelivery'),
        url(r'^infocritique/(?P<conversationID>\d+)/$', 'getInfoCritique', name = 'getInfoCritique'),


) 