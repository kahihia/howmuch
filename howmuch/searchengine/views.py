from howmuch.core.models import RequestItem
from django.http import HttpResponse
from django.shortcuts import render_to_response
from indextank.client import ApiClient
from django.core import serializers
from django.template import RequestContext
from endless_pagination.decorators import page_template
import datetime
import urllib

def defineIndex():
    api = ApiClient('http://:PAEaldYb8L2lH8@dyci1.api.searchify.com')
    index = api.get_index('idx')
    return({"api": api, "index": index})

def indexRequestItem(item):
    resource = defineIndex()
    index = resource['index']
    index.add_document(item.get_url(), {'text' : item.title, 
        'candidates' : item.getNumber_candidates(), 'state' : item.state, 'price' : item.price, 'picture' : item.get_first_picture_100x100(),
        'owner' : item.owner.username, 'pk' : item.pk })

def searchservice_test(request):
    q = urllib.unquote(request.GET.get('q', '')) 
    q = q.strip() 
    resource = defineIndex() 
    index = resource['index']
    results = [] 
    if q != '': 
        q = q.split(' ') 
        finalq = ' AND text:'.join(q)
        finalq += "*" # Wildcard at the end!
        searchresults = index.search( 'text:%s' % finalq , fetch_fields=['picture','text', 'candidates', 'state', 'price', 'owner', 'pk']) 
        
        return render_to_response('searchengine/results.html', {'searchresults' : searchresults}, context_instance = RequestContext(request) )
    return HttpResponse('{"results": "none"}') 


@page_template('searchengine/results_index_page.html')  # just add this decorator
def searchservice(request, template='searchengine/results_index.html', extra_context=None):
    q = urllib.unquote(request.GET.get('q', '')) 
    q = q.strip() 
    resource = defineIndex() 
    index = resource['index']
    results = [] 
    if q != '':
        q = q.split(' ')
        finalq = ' AND text:'.join(q)
        finalq += "*"
        searchresults = index.search( 'text:%s' % finalq , fetch_fields=['picture','text', 'candidates', 'state', 'price', 'owner', 'pk'], length=100) 
    context ={
        'items' : searchresults['results'],
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
            template, context,context_instance=RequestContext(request))
