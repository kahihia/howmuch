from django.conf.urls import patterns, include, url

from howmuch.core.forms import NewItemForm1, NewItemForm2, NewItemForm3, NewItemForm4, NewProfferForm1, NewProfferForm2
from howmuch.core.views import NewItemWizard, NewProfferWizard

FORMS_NEWITEM = [('description', NewItemForm1),
         ('clasification', NewItemForm2),
         ('delivery', NewItemForm3),
         ('pictures', NewItemForm4 )]

FORMS_NEWPROFFER = [('description', NewProfferForm1),
		('pictures', NewProfferForm2),]


urlpatterns = patterns('howmuch.core.views',
		url(r'^item/new/$', NewItemWizard.as_view(FORMS_NEWITEM)),
		#url(r'^item/new/$', 'requestItem' , name = "coreNewItem"),
		url(r'^item/(?P<itemID>\d+)/$', 'viewItem' , name = "coreViewItem"),
		url(r'^item/candidates/(?P<itemId>\d+)/$', 'viewCandidates', name="coreViewCandidates"),
		url(r'^proffer/new/(?P<itemId>\d+)/$', 'newProffer', name = "coreNewProffer"),
		#url(r'^proffer/new/$', NewProfferWizard.as_view(FORMS_NEWPROFFER)),
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