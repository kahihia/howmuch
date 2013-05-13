import urllib

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

from indextank.client import ApiClient

from howmuch.category.functions import categories_matches, categories_matches_query, rangePrice_matches_query

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
        'docid':article.get_url(),
        'all':"1",
        })
    categories = {
        'rangePrice': article.get_range_price(),
        'state':'%s' % (article.state),
        'category':'%s' % (article.category.subname),
    }
    index.update_categories(docid, categories)


def searchservice(request):
    q = urllib.unquote(request.path.split('/')[2].split('_')[0]) #Example: unquote('/%7Econnolly/') yields '/~connolly/'.
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
        cats = categories_matches()
        return render_to_response('search/results.html', 
            {'searchresults' : searchresults, 'article' : article, 'cats' : cats }, 
            context_instance = RequestContext(request) )
    return HttpResponse('Sin Resultados') 

def search_query(request, query):
    from howmuch.search.functions import * 

    index = defineIndex()['index']
    if query != '':
        article = convert_query(query)
        new_query = 'text:%s' % convert_query(query)
        new_query += "*"
        searchresults = index.search(new_query,
            fetch_fields=['text', 'img','description', 'tags','state', 'price'])
        if searchresults['matches'] == 0:
            return render_to_response('search/results.html',
                {'searchresults':searchresults, 'article' : article },
                context_instance=RequestContext(request))
        else:
            return render_to_response('search/results.html',
                {'searchresults':searchresults, 'article' : article, 'cats' : searchresults['facets']['category'].items(), 'rangePrice' : searchresults['facets']['rangePrice'].items() },
                context_instance=RequestContext(request))
    return HttpResponse('Sin Resultados')

def search_filters(request, filters):
    from howmuch.search.functions import * 

    index = defineIndex()['index']

    article = ""
    filters = convert_filters(filters)
    dic={}
    custom_filter=0
    minrange=None
    maxrange=None
    if get_state_filter(filters) != None:
        dic.update({'state':[get_state_filter(filters)]})
    if get_rangePrice_filter(filters) != None:
        if get_rangePrice_filter(filters) != "0to500" and get_rangePrice_filter(filters) != "500to1000" and get_rangePrice_filter(filters) != "1000to5000" and get_rangePrice_filter(filters) != "gte5000":
            custom_filter=1
            if get_rangePrice_filter(filters).split("to")[0] != '':
                minrange=get_rangePrice_filter(filters).split("to")[0]
            if get_rangePrice_filter(filters).split("to")[1] != '':
                maxrange=get_rangePrice_filter(filters).split("to")[1]
            if minrange>maxrange and minrange != None and maxrange != None:
                temp=minrange
                minrange=maxrange
                maxrange=temp
        else:
            dic.update({'rangePrice':[get_rangePrice_filter(filters)]})
    if get_category_filter(filters) != None:
        dic.update({'category':[get_category_filter(filters)]})
    if custom_filter == 0:
        searchresults = index.search('all:1',
            category_filters=dic,
            fetch_fields=['text', 'img','description', 'tags','state', 'price'])
    else:
        searchresults = index.search('all:1',
            category_filters=dic,
            fetch_fields=['text', 'img','description', 'tags','state', 'price'])
        lst=[]
        if minrange != None:
            if maxrange != None:
                for x in searchresults['results']:
                    if int(x['price']) > int(maxrange) or int(x['price']) < int(minrange):
                        lst.append(x)
            else:
                for x in searchresults['results']:
                    if int(x['price']) < int(minrange):
                        lst.append(x)
        else:
            if maxrange != None:
                for x in searchresults['results']:
                    if int(x['price']) > int(maxrange):
                        lst.append(x)
        for y in lst:
            searchresults['results'].remove(y)
    cats = categories_matches()
    if searchresults['matches'] == 0:
        return render_to_response('search/results.html',
            {'searchresults':searchresults, 'article' : article, 'filtros' : True, 'filters' : filters, 'cats' : cats },
            context_instance=RequestContext(request))
    else:
        if get_rangePrice_filter(filters) != None:
            return render_to_response('search/results.html',
            {'searchresults':searchresults, 'article' : article, 'filtros' : True, 'filters' : filters, 'cats' : searchresults['facets']['category'].items(), 'rangePrice' : searchresults['facets']['rangePrice'].items() },
            context_instance=RequestContext(request))
        else:
            return render_to_response('search/results.html',
            {'searchresults':searchresults, 'article' : article, 'filtros' : True, 'filters' : filters, 'cats' : cats, 'rangePrice' : searchresults['facets']['rangePrice'].items() },
            context_instance=RequestContext(request))
    return HttpResponse('Sin Resultados')

def search_query_filters(request, query, filters):
    from howmuch.search.functions import * 

    index = defineIndex()['index']

    article = convert_query(query)
    new_query = 'text:%s' % convert_query(query)
    new_query += "*"
    filters = convert_filters(filters)
    dic={}
    custom_filter=0
    minrange=None
    maxrange=None
    if get_state_filter(filters) != None:
        dic.update({'state':[get_state_filter(filters)]})
    if get_rangePrice_filter(filters) != None:
        if get_rangePrice_filter(filters) != "0to500" and get_rangePrice_filter(filters) != "500to1000" and get_rangePrice_filter(filters) != "1000to5000" and get_rangePrice_filter(filters) != "gte5000":
            custom_filter=1
            if get_rangePrice_filter(filters).split("to")[0] != '':
                minrange=get_rangePrice_filter(filters).split("to")[0]
            if get_rangePrice_filter(filters).split("to")[1] != '':
                maxrange=get_rangePrice_filter(filters).split("to")[1]
            if minrange>maxrange and minrange != None and maxrange != None:
                temp=minrange
                minrange=maxrange
                maxrange=temp
        else:
            dic.update({'rangePrice':[get_rangePrice_filter(filters)]})
    if get_category_filter(filters) != None:
        dic.update({'category':[get_category_filter(filters)]})
    if custom_filter == 0:
        searchresults = index.search(new_query,
            category_filters=dic,
            fetch_fields=['text', 'img','description', 'tags','state', 'price'])
    else:
        searchresults = index.search(new_query,
            category_filters=dic,
            fetch_fields=['text', 'img','description', 'tags','state', 'price'])
        lst=[]
        if minrange != None:
            if maxrange != None:
                for x in searchresults['results']:
                    if int(x['price']) > int(maxrange) or int(x['price']) < int(minrange):
                        lst.append(x)
            else:
                for x in searchresults['results']:
                    if int(x['price']) < int(minrange):
                        lst.append(x)
        else:
            if maxrange != None:
                for x in searchresults['results']:
                    if int(x['price']) > int(maxrange):
                        lst.append(x)
        for y in lst:
            searchresults['results'].remove(y)
            ind = index.search("docid:/article/4/Flash-Light")
            algo = ind['facets']['category'].items().pop()[0]
    if get_rangePrice_filter(filters) != None:
        if custom_filter == 0:
            return render_to_response('search/results.html',
                {'searchresults':searchresults, 'article' : article, 'filtros' : True, 'filters' : filters, 'cats' : searchresults['facets']['category'].items(), 'rangePrice' : searchresults['facets']['rangePrice'].items() },
                context_instance=RequestContext(request))
        else:
            cats=rangePrice_matches_query(new_query,dic,minrange,maxrange)         
            return render_to_response('search/results.html',
                {'searchresults':searchresults, 'article' : article, 'filtros' : True, 'filters' : filters, 'cats' : cats },
                context_instance=RequestContext(request))
    else:
        cats = categories_matches_query(new_query)
        return render_to_response('search/results.html',
        {'searchresults':searchresults, 'article' : article, 'filtros' : True, 'filters' : filters, 'cats' : cats, 'rangePrice' : searchresults['facets']['rangePrice'].items() },
        context_instance=RequestContext(request))
    #return HttpResponse('Sin Resultados')