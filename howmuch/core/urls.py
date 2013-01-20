from django.conf.urls import patterns, include, url

from howmuch.core.forms import NewItemForm1, NewItemForm2, NewItemForm3, NewItemForm4, NewItemForm5, NewItemForm6, NewItemForm7
from howmuch.core.views import Post

FORMS_NEWITEM = [('title', NewItemForm1),
        ('price', NewItemForm2),
        ('quantity', NewItemForm3),
        ('description', NewItemForm4),
        ('clasification', NewItemForm5),
        ('delivery', NewItemForm6),
        ('pictures', NewItemForm7)]

urlpatterns = patterns('howmuch.core.views',
        url(r'^item/new/$', NewItemWizard.as_view(FORMS_NEWITEM)),
        url(r'^item/(?P<itemID>\d+)/(?P<title_url>[a-zA-Z0-9_+-]+)/$', 'viewItem' , name = "coreViewItem"),
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