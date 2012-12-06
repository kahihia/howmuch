from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.messages.views',
        url(r'^(?P<conversationID>\d+)/$', 'newMessage' , name = "messagesNewMessage"),
        url(r'^inbox/$', 'viewInbox' , name = "messagesViewInbox"),     
        url(r'^infobuyer/(?P<conversationID>\d+)/$', 'getInfoBuyer', name = 'messagesGetInfoBuyer'),
        url(r'^infoseller/(?P<conversationID>\d+)/$', 'getInfoSeller', name = 'messagesGetInfoSeller'),
        url(r'^infoconfirmpay/(?P<conversationID>\d+)/$', 'getInfoConfirmPay', name = 'messagesGetInfoConfirmPay'),
        url(r'^infoconfirmdelivery/(?P<conversationID>\d+)/$', 'getInfoConfirmDelivery', name = 'messagesGetInfoConfirmDelivery'),
        url(r'^infocritique/(?P<conversationID>\d+)/$', 'getInfoCritique', name = 'messagesGetInfoCritique')
) 