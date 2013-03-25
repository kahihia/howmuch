from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from paypal.standard.forms import PayPalPaymentsForm

def paypal(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "0.01",
        "item_name": "Articulo 1",
        "invoice": "jajaj9",
        "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
        "return_url": "http://www.comprateca.com/return/",
        "cancel_return": "http://www.comprateca.com/cancelreturn",

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render_to_response("pays/payment.html", context)
