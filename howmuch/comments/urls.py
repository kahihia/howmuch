from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.comments.views',

	    url(r'^post/(?P<articleID>\d+)/$', 'post', name='post_comment'),  

) 