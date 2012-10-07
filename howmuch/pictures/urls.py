from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('howmuch.pictures.views',
		url(r'^addpicture/proffer/(?P<profferID>\d+)/$','addPictureProffer', name = "addPicture"),
		url(r'^addpicture/requestitem/(?P<requestItemID>\d+)/$','addPictureRequestItem', name = "addPicture"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
