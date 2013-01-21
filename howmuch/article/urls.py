from django.conf.urls import patterns, include, url

from howmuch.article.forms import ArticleForm1, ArticleForm2, ArticleForm3, ArticleForm4, ArticleForm5, ArticleForm6, ArticleForm7
from howmuch.article.views import Post

FORMS_NEWITEM = [('title', ArticleForm1),
        ('price', ArticleForm2),
        ('quantity', ArticleForm3),
        ('description', ArticleForm4),
        ('clasification', ArticleForm5),
        ('delivery', ArticleForm6),
        ('pictures', ArticleForm7)]

urlpatterns = patterns('howmuch.article.views',
        url(r'^post/$', Post.as_view(FORMS_NEWITEM)),
        url(r'^(?P<itemID>\d+)/(?P<title_url>[a-zA-Z0-9_+-]+)/$', 'view' , name = "viewarticle"),
        url(r'^candidates/(?P<itemId>\d+)/$', 'candidates', name="listofcandidates"),
        url(r'^offer/(?P<itemId>\d+)/$', 'offer', name = "addofferforarticle"),
        url(r'^assignment/(?P<itemId>\d+)/(?P<candidateID>\d+)/$','assignment', name = "addassignmentforarticle"),
) 