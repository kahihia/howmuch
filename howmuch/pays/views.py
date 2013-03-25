from django.shortcuts import render_to_response
from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm

def paypal(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "0.01",
        "item_name": "Articulo 1",
        "invoice": "1",
        "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
        "return_url": "http://www.example.com/your-return-location/",
        "cancel_return": "http://www.example.com/your-cancel-location/",

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render_to_response("pays/payment.html", context)
