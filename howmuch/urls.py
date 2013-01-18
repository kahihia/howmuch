from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$',  login),
    url(r'^logout/$', logout),
    url(r'^', include('howmuch.core.urls')),
    url(r'^profile/', include('howmuch.perfil.urls')),
    url(r'^messages/', include('howmuch.messages.urls')),
    url(r'^pictures/', include('howmuch.pictures.urls')),
    url(r'^prestige/', include('howmuch.prestige.urls')),
    url(r'^search/', include('howmuch.searchengine.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^notifications/', include('howmuch.notifications.urls')),
    url(r'^config/', include('howmuch.config.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
