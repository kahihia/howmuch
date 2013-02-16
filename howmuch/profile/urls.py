from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('howmuch.profile.views',
        url(r'^(?P<username>\w+)/$', 'viewProfile', name = 'perfilViewProfile'),
        #List of followings
        url(r'^e/following/$', 'following', name = 'following'),
        #Follow Article
        url(r'^e/follow/(?P<articleID>\d+)/$', 'follow', name="follow article"),
        #Unfollow Article
    	url(r'^e/unfollow/(?P<articleID>\d+)/$', 'unfollow', name="unfollow article"),
        url(r'^e/edit/$', 'edit' , name = "profileEdit"),
        url(r'^e/newaddress/$', 'newAddress', name = 'perfilNewAddress'),
        url(r'^e/newphone/$', 'newPhone', name = 'perfilNewPhone'),
        url(r'^e/newaccountbank', 'newAccountBank', name='perfilNewAccountBank'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



