from django.conf.urls import patterns, include, url

from howmuch.article.views import post

urlpatterns = patterns('howmuch.article.views',
        url(r'^post/$','post', name ="addPost"),
        url(r'^(?P<articleID>\d+)/(?P<title_url>[a-zA-Z0-9_+-]+)/$', 'view' , name = "viewarticle"),
        url(r'^(?P<articleID>\d+)/(?P<title_url>[a-zA-Z0-9_+-]+)/edit/$', 'edit' , name = "editarticle"),
        url(r'^candidates/(?P<articleID>\d+)/$', 'candidates', name="listofcandidates"),
        url(r'^offer/(?P<articleID>\d+)/$', 'offer', name = "addofferforarticle"),
        url(r'^assignment/(?P<articleID>\d+)/(?P<candidateID>\d+)/$','assignment', name = "addassignmentforarticle"),
) 