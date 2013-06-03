from django import forms
from django.forms import ModelForm, Textarea, ClearableFileInput, TextInput

from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, Critique


class ConfirmPayForm(ModelForm):
    class Meta:
        model = ConfirmPay
        exclude = ('owner' , 'assignment', 'date',)
        widgets = {
        'amount' : TextInput(attrs={'class':'width-100'}),
        'message' : Textarea(attrs={'class':'width-100','style':'height:10em'}),
        'picture' : ClearableFileInput(attrs={'class':'text password width-100'}),
        }

class ConfirmDeliveryForm(ModelForm):
    class Meta:
        model = ConfirmDelivery
        exclude = ('owner', 'assignment', 'date',)
        widgets = {
        'message' : Textarea(attrs={'id':'confirm-delivery-file-upload-input','class':'width-100','style':'height:10em'}),
        'picture' : ClearableFileInput(attrs={'class':'text password width-100'}),
        }

class CritiqueForm(ModelForm):
    class Meta:
        model = Critique
        exclude = ('de', 'to', 'assignment', 'date',)
        widgets = {
        'message' : Textarea(attrs={'class':'span12'})
        }
