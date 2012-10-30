from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.backend.views',
		url(r'^salescount/$', 'salesCount' , name = "backendSalesCountView"),	
		url(r'^inboxcount/$', 'inboxCount', name = "backendInboxCountView"),
		url(r'^purchasescount/$', 'purchasesCount', name = "backendPurchasesCountView"),	
) 