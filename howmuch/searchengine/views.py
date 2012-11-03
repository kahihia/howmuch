from howmuch.core.models import RequestItem
from django.http import HttpResponse
from django.shortcuts import render_to_response
from indextank.client import ApiClient
from django.core import serializers
from django.template import RequestContext
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

def indexsearch(request):
	resource = defineIndex()
	items = RequestItem.objects.all()
	index = resource['index']

	for item in items:
		try:
			itemtitle = str(item.title)
		except UnicodeEncodeError:
			itemtitle = False
		if itemtitle:
			index.add_document(str(obj.pk), {'text': objtitle})
	return(HttpResponse('Indexing: %s' % datetime.datetime.now() ))

def searchservice(request):
	q = urllib.unquote(request.GET.get('q', '')) # uncode the request
	q = q.strip() # Get rid of white space, it will mess with results from Searchify
	resource = defineIndex() # Grab our Searchify object
	index = resource['index']
	results = [] # Hold our results
	if q != '': # If q is a string
		q = q.split(' ') # split by space into an array
		# Join it together again, with an AND clause
		# We want each word to be seperated by an AND clause
		# This will make sure that all words appear in the title
		# But the last word will have a wildcard at the end,
		# because the user is still typing.
		finalq = ' AND text:'.join(q)
		finalq += "*" # Wildcard at the end!
		searchresults = index.search( 'text:%s' % finalq , fetch_fields=['picture','text', 'candidates', 'state', 'price', 'owner', 'pk']) 
		
		return render_to_response('searchengine/results.html', {'searchresults' : searchresults}, context_instance = RequestContext(request) )
	return HttpResponse('{"results": "none"}') 