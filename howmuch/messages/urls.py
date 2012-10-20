from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.messages.views',
		url(r'^(?P<conversationID>\d+)/$', 'newMessage' , name = "messagesNewMessage"),
		url(r'^inbox/$', 'viewInbox' , name = "messagesViewInbox"),		
) 