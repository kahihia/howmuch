from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.problems.views',

		url(r'^$', 'problem_out', name='report problem out'),
	    url(r'^problem/(?P<assignmentID>\d+)/$', 'problem', name = 'post problem'), 
	    url(r'^reply/(?P<problemID>\d+)/$','reply', name = 'post reply'),
	    url(r'^action/(?P<problemID>\d+)/$', 'action', name = 'post action'),
	    url(r'^my/$', 'my_problems', name = 'my problems'),
)