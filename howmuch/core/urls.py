from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.core.views',
		url(r'^item/new/$', 'requestItem' , name = "coreNewItem"),
		url(r'^item/candidates/(?P<itemId>\d+)/$', 'viewCandidates', name="coreViewCandidates"),
		url(r'^proffer/new/(?P<itemId>\d+)/$', 'newProffer', name = "coreNewProffer"),
		url(r'^assignment/new/(?P<itemId>\d+)/(?P<candidateID>\d+)/$','newAssignment', name = "coreNewAssignment"),
		url(r'^$','home', name = "coreHome"),
) 