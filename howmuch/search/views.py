from django.http import HttpResponse
from django.shortcuts import render_to_response
from indextank.client import ApiClient
from django.template import RequestContext
import urllib

def defineIndex():
    api = ApiClient('http://:rMESs36rCF83rc@8ytx3.api.searchify.com')
    index = api.get_index('idx')
    return({"api": api, "index": index})

def index_article(article):
    resource = defineIndex()
    index = resource['index']
    index.add_document(article.get_url(), {'text' : article.title, 
        'candidates' : article.getNumber_candidates(), 'state' : article.state, 'price' : article.price,
        'owner' : article.owner.username, 'pk' : article.pk })

def searchservice(request):
    q = urllib.unquote(request.GET.get('q', '')) 
    q = q.strip() 
    resource = defineIndex() 
    index = resource['index']
    results = [] 
    if q != '': 
        q = q.split(' ') 
        finalq = ' AND text:'.join(q)
        finalq += "*" 
        searchresults = index.search( 'text:%s' % finalq , fetch_fields=['text', 'candidates', 'state', 'price', 'owner', 'pk']) 
        return render_to_response('search/results.html', {'searchresults' : searchresults, 'article' : q }, context_instance = RequestContext(request) )
    return HttpResponse('{"results": "none"}') 


