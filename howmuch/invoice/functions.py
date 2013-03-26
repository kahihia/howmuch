import datetime

from django.shortcuts import get_object_or_404

from howmuch.invoice.models import Charge, Invoice
from howmuch.settings import COMMISSION, DAYS_LIMIT_INVOICE

#Cuando el usuario paga la factura, se cambian los status de la factura pagada
def change_status_invoice(invoice):
	invoice.is_paid = True
	invoice.save()

#Se verifica que el total de la factura sea menor al limite de credito del usuario
def check_invoice(invoice):
	import datetime
	if invoice.total > invoice.owner.profile.credit_limit:
		invoice.due_date = datetime.date.today() + datetime.timedelta(days=DAYS_LIMIT_INVOICE)
		invoice.save()

#Generar cargo al usuario para determinada asignacion
def generate_charge(assignment, price, invoice):
	#Se crea el cargo
	charge = Charge.objects.create(owner=assignment.owner, assignment=assignment, 
		period=assignment.owner.profile.current_invoice, price=price, 
		commission=price * COMMISSION)
	#Se agrega el cargo a la factura actual del usuario
	invoice.charges.add(charge)
	#Se actualiza el total del cargo
	invoice.total += charge.commission
	invoice.save()


#Generar Factura, estas se generan cada vez que el usuario ha pagado
def generate_invoice(user):
	period = user.profile.current_invoice + 1
	try:
		invoice = Invoice.objects.get(owner=user, period=period)
	except Invoice.DoesNotExist:
		invoice = Invoice.objects.create(owner=user, period=period, 
			reference=generate_reference(user))
		invoice.invoice = generate_number_invoice(invoice.pk)
		invoice.save()
	#Se actualiza el current_invoice del usuario
	user.profile.current_invoice = period
	user.profile.save()

#Generar Referencia Alfanumerica de la Factura en el formato 'userID' + 'month' + 'year'
def generate_reference(user):
	return '%07d%s%s' % (user.pk, datetime.datetime.now().month, datetime.datetime.now().year) 


def generate_number_invoice(invoiceID):
	import hashlib
	number = hashlib.sha224(str(invoiceID)).hexdigest() 
	return number[17:27]


#Unlock account
def unlock_account(user):
	user.profile.is_block = False
	user.profile.save()
















