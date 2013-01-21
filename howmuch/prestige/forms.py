from django import forms
from django.forms import ModelForm

from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, PrestigeLikeBuyer, PrestigeLikeSeller

class ConfirmPayForm(ModelForm):
    class Meta:
        model = ConfirmPay
        exclude = ('owner' , 'assignment', 'date')

class ConfirmDeliveryForm(ModelForm):
    class Meta:
        model = ConfirmDelivery
        exclude = ('owner', 'assignment', 'date', )

class PrestigeLikeBuyerForm(ModelForm):
    class Meta:
        model = PrestigeLikeBuyer
        exclude = ('de', 'to', 'assignment', 'date', )

class PrestigeLikeSellerForm(ModelForm):
    class Meta:
        model = PrestigeLikeSeller
        exclude = ('de', 'to', 'assignment', 'date')

