import datetime

from django.shortcuts import get_object_or_404

from howmuch.invoice.models import Charge, Invoice
from howmuch.settings import COMMISSION

#Generar Periodo en formato MM/YY
def get_period():
	return '%s/%s' % (datetime.datetime.now().month, datetime.datetime.now().year)


#Generar cargo al usuario para determinada asignacion
def generate_charge(assignment, price, invoice):
	charge = Charge.objects.create(owner=assignment.owner, assignment=assignment, period=get_period(), price=price)
	invoice.charges.add(charge)
	return charge


#Generar Comision
def generate_commission(assignment):
	assignment.charge.commission = assignment.charge.price * COMMISSION
	assignment.charge.save()


#Generar Referencia Alfanumerica de la Factura en el formato 'userID' + 'month' + 'year'
def generate_reference(user):
	return '%05d%s%s' % (user.pk, datetime.datetime.now().month, datetime.datetime.now().year) 


#Generar Factura si no existe
def generate_invoice(user):
	period = get_period()
	try:
		invoice = Invoice.objects.get(owner=user, period=period)
	except Invoice.DoesNotExist:
		invoice = Invoice.objects.create(owner=user, period=period, reference=generate_reference(user))
	return invoice





