from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.core.views',
		url(r'^item/new/$', 'requestItem' , name = "coreNewItem"),
		url(r'^item/candidates/(?P<itemId>\d+)/$', 'viewCandidates', name="coreViewCandidates"),
		url(r'^proffer/new/(?P<itemId>\d+)/$', 'newProffer', name = "coreNewProffer"),
		url(r'^assignment/new/(?P<itemId>\d+)/(?P<candidateID>\d+)/$','newAssignment', name = "coreNewAssignment"),
		#Purchase Views
		url(r'^purchases/published/$', 'publishedPurchasesView' , name = "corePublishedPurchasesView"),
		url(r'^purchases/process/$', 'processPurchasesView' , name = "coreProcessPurchasesView"),
		url(r'^purchases/completed/$', 'completedPurchasesView' , name = "coreCompletedPurchasesView"),
		#Sales Views
		url(r'^sales/possible/$', 'possibleSalesView' , name = "corePossibleSalesView"),
		url(r'^sales/process/$', 'processSalesView' , name = "coreProcessSalesView"),
		url(r'^sales/completed/$', 'completedSalesView' , name = "coreCompletedSalesView"),

		url(r'^$','home', name = "coreHome"),
) 