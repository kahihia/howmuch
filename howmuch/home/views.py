from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
	from howmuch.home.functions import get_last_articles

	return render_to_response('home/home.html', 
		{'articles' : get_last_articles()}, context_instance=RequestContext(request))