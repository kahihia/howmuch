from howmuch.core.models import RequestItem
from django.http import HttpResponse
from indextank.client import ApiClient
from django.core import serializers
import datetime

def defineIndex():
	api = ApiClient('http://:PAEaldYb8L2lH8@dyci1.api.searchify.com')
	index = api.get_index('idx')
	return({"api": api, "index": index})

def indexsearch(request):
	resource = defineIndex()
	allObjs = RequestItem.objects.all()
	index = resource['index']

	for obj in allObjs:
		try:
			objtitle = str(obj.title)
		except UnicodeEncodeError:
			objtitle = False
		if objtitle:
			index.add_document(str(obj.pk), {'text': objtitle})
	return(HttpResponse('Indexing: %s' % datetime.datetime.now() ))

def searchservice(request):
	q = unquote(request.GET.get('q', '')) # uncode the request
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
		searchresults = index.search( 'text:%s' % finalq ) # Run the search
		for result in searchresults['results']: # For each searchresults
			try:
				# Grab the object in django, if it's published!
				obj = RequestItem.objects.get(pk=result['docid'])
				results.append(obj)
			except RequestItem.DoesNotExist: # Model wasn't found.
				pass
		# Return the results in a serialized JSON response.
		return HttpResponse(serializers.serialize("json", results))
	# Or some raw JSON saying none were found.
	return HttpResponse('{"results": "none"}') 