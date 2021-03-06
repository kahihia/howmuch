from django.shortcuts import render_to_response
from django.template import RequestContext

def privacy(request):
	return render_to_response('about/privacy.html',{},
		context_instance=RequestContext(request))


def terms(request):
	return render_to_response('about/terms.html',{},
		context_instance=RequestContext(request))


def faq(request):
	return render_to_response('about/faq.html',{},
		context_instance=RequestContext(request))

def contact(request):
	return render_to_response('about/contact.html', {},
		context_instance=RequestContext(request))
