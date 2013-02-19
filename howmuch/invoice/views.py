from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Sum

from howmuch.invoice.models import Charge, Invoice

def invoice(request):
	invoice = Invoice.objects.get(owner=request.user, period='2/2013')

	charges = []
	
	c_feb13 = invoice.charges.all()
	t_feb13 = invoice.charges.all().aggregate(Sum('commission'))

	charges.append({'charges' : c_feb13, 'total' : t_feb13})

	return render_to_response('invoice/invoice.html', {'charges' : charges}, 
		context_instance=RequestContext(request))
