from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from howmuch.invoice.models import Charge, Invoice
from howmuch.invoice.forms import PayForm
from howmuch.invoice.functions import change_status_invoice, generate_invoice


def invoice(request):
	period = request.user.profile.current_invoice
	current_invoice = request.user.profile.get_current_invoice()
	return render_to_response('invoice/invoice.html', {'current_invoice' : current_invoice}, 
		context_instance=RequestContext(request))

def pay(request, invoiceID):
	invoice = get_object_or_404(Invoice, pk=invoiceID,owner=request.user)
	if request.method == 'POST':
		form = PayForm(request.POST)
		if form.is_valid():
			pay = form.save(commit=False)
			pay.owner = request.user
			pay.invoice = invoice
			pay.save()
			#Se cambia el status del Invoice
			change_status_invoice(invoice)
			#Se genera una nueva factura
			generate_invoice(request.user)
			return HttpResponse('Pago realizado Correctamente')
	else:
		form = PayForm()
	return render_to_response('invoice/pay.html',{'form':form}, 
		context_instance=RequestContext(request))

