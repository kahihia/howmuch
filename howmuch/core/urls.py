from django.conf.urls import patterns, include, url

from howmuch.core.forms import NewItemNewForm1, NewItemNewForm2, NewItemNewForm3, NewItemNewForm4, NewItemNewForm5, NewItemNewForm6, NewItemNewForm7
from howmuch.core.views import NewItemWizard

FORMS_NEWITEM_NEW = [('title', NewItemNewForm1),
        ('price', NewItemNewForm2),
        ('quantity', NewItemNewForm3),
        ('description', NewItemNewForm4),
        ('clasification', NewItemNewForm5),
        ('delivery', NewItemNewForm6),
        ('pictures', NewItemNewForm7)]

urlpatterns = patterns('howmuch.core.views',
        #url(r'^item/new/$', NewItemWizard.as_view(FORMS_NEWITEM)),
        url(r'^item/new/$', NewItemWizard.as_view(FORMS_NEWITEM_NEW)),
        #url(r'^item/new/$', 'requestItem' , name = "coreNewItem"),
        url(r'^item/(?P<itemID>\d+)/(?P<title_url>[a-zA-Z0-9_+-]+)/$', 'viewItem' , name = "coreViewItem"),
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