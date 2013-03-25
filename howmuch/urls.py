from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin

from howmuch.tags.functions import tags_json

admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    url(r'^', include('howmuch.home.urls')),

    url(r'^login/$',  login),
    url(r'^logout/$', logout, {'next_page' : '/'}),

    url(r'^test/$', 'direct_to_template', {'template': 'test.html'}),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^facebook/', include('django_facebook.urls')),
    
    url(r'^about/', include('howmuch.about.urls')),
    url(r'^account/', include('howmuch.account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^article/', include('howmuch.article.urls')),
    url(r'^comments/', include('howmuch.comments.urls')),
    url(r'^config/', include('howmuch.config.urls')),
    url(r'^invoice/', include('howmuch.invoice.urls')),
    url(r'^messages/', include('howmuch.messages.urls')),
    url(r'^notifications/', include('howmuch.notifications.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^pays/', include('howmuch.pays.urls')),
    url(r'^prestige/', include('howmuch.prestige.urls')),
    url(r'^problems/', include('howmuch.problems.urls')),
    url(r'^profile/', include('howmuch.profile.urls')),
    url(r'^search/', include('howmuch.search.urls')),
    url(r'^tags/$', tags_json),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
