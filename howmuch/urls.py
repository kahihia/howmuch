from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('howmuch.core.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^login/$',  login),
    url(r'^logout/$', logout),
	url(r'^chaining/', include('howmuch.smart_selects.urls')),
	url(r'^pictures/', include('howmuch.Pictures.urls')),
	
    # Examples:
    # url(r'^$', 'howmuch.views.home', name='home'),
    # url(r'^howmuch/', include('howmuch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
