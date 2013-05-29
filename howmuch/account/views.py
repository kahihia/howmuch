from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_list_or_404
from django.template import RequestContext

from howmuch.article.models import Article, Offer, Assignment

@login_required(login_url='/login/')
def purchases_list(request):
    items = Article.objects.filter(owner=request.user)
    publishedPurchases = []
    processPurchases = []
    completedPurchases = []
    for item in items:
        #Lista de compras publicadas
        if not item.has_assignment():
            publishedPurchases.append(item)
        #Lista de compras en proceso
        elif item.has_assignment() and not item.has_been_completed():
            processPurchases.append(item)
        #Lista de compras terminadas
        elif item.has_been_completed():
            completedPurchases.append(item)
    return render_to_response('account/purchases_list.html', 
        {'publishedPurchases' : publishedPurchases, 'processPurchases' : processPurchases, 
        'completedPurchases' : completedPurchases}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def sales_list(request):
    #Asignaciones 
    processSales = Assignment.objects.filter(owner = request.user, status__in = ["0","1","2","3"])
    #Transacciones Terminadas
    completedSales = Assignment.objects.filter(owner = request.user, status = "4")
    return render_to_response('account/sales_list.html',{'processSales' : processSales,
        'completedSales' : completedSales}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def offers_list(request):
    offers = Offer.objects.filter(owner=request.user)
    #Ofertas realizadas
    offer_list = []
    for offer in offers:
        if offer.is_open():
            offer_list.append(offer)
    return render_to_response('account/offers_list.html', {'offer_list':offer_list}, 
        context_instance=RequestContext(request))

    


