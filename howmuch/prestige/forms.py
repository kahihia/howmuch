from django import forms
from django.forms import ModelForm

from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, Critique


class ConfirmPayForm(ModelForm):
    class Meta:
        model = ConfirmPay
        exclude = ('owner' , 'assignment', 'date',)

class ConfirmDeliveryForm(ModelForm):
    class Meta:
        model = ConfirmDelivery
        exclude = ('owner', 'assignment', 'date',)

class CritiqueForm(ModelForm):
    class Meta:
        model = Critique
        exclude = ('de', 'to', 'assignment', 'date',)
