import urllib

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

from indextank.client import ApiClient



def defineIndex():
    api = ApiClient('http://:rMESs36rCF83rc@8ytx3.api.searchify.com')
    index = api.get_index(settings.SEARCHIFY_INDEX)
    return({"api": api, "index": index})

def index_article(article):
    resource = defineIndex()
    index = resource['index']
    index.add_document(article.get_url(), {
        'text' : article.title, 
        'img' : article.get_first_picture_url(),
        'description' : article.description[:100],
        'tags' : article.get_list_tags(),
        'state' : article.state, 
        'price' : article.price})

def index_article2(article):
    index = defineIndex()['index']
    docid = article.get_url()
    index.add_document(docid,{ #docid
        'text': article.title, #article title
        'img': article.get_first_picture_url(), #first picture of the article
        'description': article.description[:100], #first 100 characters of the description
        'tags': article.get_list_tags(), #string of tags separated by comma
        'price':article.price, #price of article
        })
    categories = {
        rangePrice: article.get_range_price(),
        state:'%s' % (article.state),
        category:'%s' % (article.category),
    }
    index.update_categories(docid, categories)


def searchservice(request):
    q = urllib.unquote(request.GET.get('q', '')) 
    q = q.strip() 
    article = q
    resource = defineIndex() 
    index = resource['index']
    results = [] 
    if q != '': 
        q = q.split(' ') 
        finalq = ' AND text:'.join(q)
        finalq += "*" 
        searchresults = index.search( 'text:%s' % finalq , 
            fetch_fields=['text', 'img','description', 'tags','state', 'price']) 
        return render_to_response('search/results.html', 
            {'searchresults' : searchresults, 'article' : article }, 
            context_instance = RequestContext(request) )
    return HttpResponse('{"results": "none"}') 


