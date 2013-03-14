from django import forms
from django.forms import ModelForm, Textarea

from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, Critique


class ConfirmPayForm(ModelForm):
    class Meta:
        model = ConfirmPay
        exclude = ('owner' , 'assignment', 'date',)
        widgets = {
        'message' : Textarea(attrs={'class':'span12'})
        }

class ConfirmDeliveryForm(ModelForm):
    class Meta:
        model = ConfirmDelivery
        exclude = ('owner', 'assignment', 'date',)
        widgets = {
        'message' : Textarea(attrs={'class':'span12'})
        }

class CritiqueForm(ModelForm):
    class Meta:
        model = Critique
        exclude = ('de', 'to', 'assignment', 'date',)
        widgets = {
        'message' : Textarea(attrs={'class':'span12'})
        }
