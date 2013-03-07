from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('howmuch.profile.views',
        url(r'^(?P<username>\w+)/$', 'view_profile', name = 'view profile'),
        #List of followings
        url(r'^e/following/$', 'following', name = 'following'),
        #Follow Article
        url(r'^e/follow/(?P<articleID>\d+)/$', 'follow', name='follow article'),
        #Unfollow Article
    	url(r'^e/unfollow/(?P<articleID>\d+)/$', 'unfollow', name='unfollow article'),
        url(r'^e/edit/$', 'edit' , name = 'edit profile'),
        url(r'^e/newaddress/$', 'new_address', name = 'new address'),
        url(r'^e/editaddress/(?P<addressID>\d+)/$', 'edit_address', name= 'edit address'),
        url(r'^e/newphone/$', 'new_phone', name = 'new phone'),
        url(r'^e/editphone/(?P<phoneID>\d+)/$', 'edit_phone', name= 'edit phone'),
        url(r'^e/newaccountbank', 'new_account_bank', name='new account bank'),
        url(r'^e/editbank/(?P<bankID>\d+)/$', 'edit_account_bank', name='edit account bank'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



