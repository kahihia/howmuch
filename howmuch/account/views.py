from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from howmuch.article.models import Article, Offer, Assignment

@login_required(login_url="/login/")
def publishedPurchases(request):
    items = Article.objects.filter(owner = request.user)
    publishedPurchases = []
    for item in items:
        if not item.has_assignment():
            publishedPurchases.append(item)
    return render_to_response('account/publishedPurchases.html', {'publishedPurchases' : publishedPurchases }, context_instance = RequestContext(request))


@login_required(login_url="/login/")
def processPurchases(request):
    items = Article.objects.filter(owner = request.user)
    processPurchases = []
    for item in items:
        if item.has_assignment() and not item.has_been_completed():
            processPurchases.append(item)
    return render_to_response('account/processPurchases.html', {'processPurchases' : processPurchases }, context_instance = RequestContext(request))


@login_required(login_url="/login/")
def completedPurchases(request):
    items = Article.objects.filter(owner = request.user)
    completedPurchases = []
    for item in items:
        if item.has_been_completed():
            completedPurchases.append(item)
    return render_to_response('account/completedPurchases.html', {'completedPurchases' : completedPurchases}, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def possibleSales(request):
    items = Offer.objects.filter(owner = request.user )
    possibleSales = []
    for item in items:
        if item.is_open():
            possibleSales.append(item)
    return render_to_response('account/possibleSales.html', {'possibleSales' : possibleSales }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def processSales(request):
    processSales = Assignment.objects.filter(owner = request.user, status__in = ["0","1","2","3"])
    return render_to_response('account/processSales.html', {'processSales' : processSales}, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def completedSales(request):
    completedSales = Assignment.objects.filter(owner = request.user, status = "4")
    return render_to_response('account/completedSales.html', {'completedSales' : completedSales }, context_instance = RequestContext(request))



