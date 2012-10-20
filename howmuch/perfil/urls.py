from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('howmuch.perfil.views',
		url(r'^edit/$', 'edit' , name = "profileEdit"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



