from django import forms 
from django.forms import ModelForm

from howmuch.invoice.models import Pay

class PayForm(ModelForm):
	class Meta:
		model = Pay
		exclude = ('owner', 'date', 'invoice')