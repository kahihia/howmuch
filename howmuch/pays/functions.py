from howmuch.settings import PAYPAL_RECEIVER_EMAIL, URL_OFFICIAL_SITE


#Regresa el formulario que contiene el boton para hacer el pago directo a paypal de la factura
def get_paypal_form(invoice):
	from django.core.urlresolvers import reverse
	from paypal.standard.forms import PayPalPaymentsForm

	paypal_dict = {
		"business" : PAYPAL_RECEIVER_EMAIL,
		"amount" : "%s" % (str(invoice.total)),
		"item_name" : "%s" % (invoice.get_item_name()),
		"invoice" : invoice.invoice ,
		"notify_url" : "%s%s" % (URL_OFFICIAL_SITE, reverse('paypal-ipn')),
		"return_url" : "%s/pays/done" % (URL_OFFICIAL_SITE),
		"cancel_return" : "%s/pays/cancel" % (URL_OFFICIAL_SITE),
	}

	form = PayPalPaymentsForm(initial=paypal_dict)

	return form
