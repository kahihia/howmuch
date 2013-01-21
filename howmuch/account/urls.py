from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.account.views',
        url(r'^purchases/published/$', 'publishedPurchases' , name = "publishedpurchases"),
        url(r'^purchases/process/$', 'processPurchases' , name = "processpurchases"),
        url(r'^purchases/completed/$', 'completedPurchases' , name = "completedpurchases"),
        url(r'^sales/possible/$', 'possibleSales' , name = "possiblesales"),
        url(r'^sales/process/$', 'processSales' , name = "processsales"),
        url(r'^sales/completed/$', 'completedSales' , name = "completedsales"),
) 