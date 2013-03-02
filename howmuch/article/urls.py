from django.conf.urls import patterns, include, url

from howmuch.article.views import post

urlpatterns = patterns('howmuch.article.views',
        url(r'^post/$','post', name ="addPost"),
        url(r'^(?P<articleID>\d+)/(?P<title_url>[a-zA-Z0-9_+-]+)/$', 'view' , name = 'viewarticle'),
        url(r'^(?P<articleID>\d+)/(?P<title_url>[a-zA-Z0-9_+-]+)/edit/$', 'edit' , name = 'editarticle'),
        url(r'^candidates/(?P<articleID>\d+)/$', 'candidates', name='candidates'),
        url(r'^offer/(?P<articleID>\d+)/$', 'offer', name = 'offer'),
        url(r'^offer/view/(?P<offerID>\d+)/$', 'offer_view', name = 'offer_view'),
        url(r'^myoffer/(?P<offerID>\d+)/$', 'my_offer', name='my_offer'),
        url(r'^assignment/(?P<articleID>\d+)/(?P<candidateID>\d+)/$','assignment', name = 'addassignmentforarticle'),
        url(r'^tags/$','get_article_tags', name='get_article_tags'),
) 