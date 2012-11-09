from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('howmuch.perfil.views',
		url(r'^(?P<username>\w+)/$', 'viewProfile', name = 'perfilViewProfile'),
		url(r'^e/edit/$', 'edit' , name = "profileEdit"),
		url(r'^newaddress/$', 'newAddress', name = 'perfilNewAddress'),
		url(r'^newphone/$', 'newPhone', name = 'perfilNewPhone'),
		url(r'^newaccountbank', 'newAccountBank', name='perfilNewAccountBank'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



