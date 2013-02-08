from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('howmuch.home.urls')),

    url(r'^login/$',  login),
    url(r'^logout/$', logout),

    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^account/', include('howmuch.account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^article/', include('howmuch.article.urls')),
    url(r'^config/', include('howmuch.config.urls')),
    url(r'^messages/', include('howmuch.messages.urls')),
    url(r'^comments/', include('howmuch.comments.urls')),
    url(r'^notifications/', include('howmuch.notifications.urls')),
    url(r'^prestige/', include('howmuch.prestige.urls')),
    url(r'^profile/', include('howmuch.profile.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
