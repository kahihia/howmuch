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
        'rangePrice': article.get_range_price(),
        'state':'%s' % (article.state),
        'category':'%s' % (article.category.subname),
    }
    index.update_categories(docid, categories)


def searchservice(request):
    q = urllib.unquote(request.GET.get('q', '')) #Example: unquote('/%7Econnolly/') yields '/~connolly/'.
    q = q.strip() #Return a copy of the string with the leading and trailing characters removed. 
    article = q
    resource = defineIndex() 
    index = resource['index']
    results = [] 
    if q != '': 
        q = q.split(' ') 
        finalq = ' AND text:'.join(q) #Example 'juan AND text:carlos AND text:cayetano'
        finalq += "*" 
        searchresults = index.search( 'text:%s' % finalq , 
            fetch_fields=['text', 'img','description', 'tags','state', 'price']) 
        return render_to_response('search/results.html', 
            {'searchresults' : searchresults, 'article' : article }, 
            context_instance = RequestContext(request) )
    return HttpResponse('Sin Resultados') 

def search(request, query, filters):
    from howmuch.search.functions import * 

    index = defineIndex()['index']
    if query != '':
        new_query = 'text:%s' % convert_query(query)
        new_query += "*"
        filters = convert_filters(filters)
        searchresults = index.search(new_query,
                                    category_filters={
                                    'state':[get_state_filter(filters)],
                                    'rangePrice':[get_rangePrice_filter(filters)],
                                    'category':[get_category_filter(filters)],
                                    },
                                    fetch_fields=['text', 'img','description', 'tags','state', 'price'])
        return render_to_response('search/results.html',
                {'searchresults':searchresults},
                context_instance=RequestContext(request))
    return HttpResponse('Sin Resultados')


    


