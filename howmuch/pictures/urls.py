from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('howmuch.pictures.views',
		url(r'^addpicture/(?P<profferID>\d+)/$','addPicture', name = "addPicture"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
