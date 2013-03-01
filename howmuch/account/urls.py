from django.conf.urls import patterns, include, url

urlpatterns = patterns('howmuch.account.views',
		url(r'^offers/$','offers_list', name="offers_list"),
        url(r'^purchases/$', 'purchases_list' , name = "purchases_list"),
        url(r'^sales/$', 'sales_list' , name = "sales_list"),
) 