from django import forms
from django.forms import ModelForm
from howmuch.prestige.models import PayConfirm, DeliveryConfirm, Prestige

class PayConfirmForm(ModelForm):
	class Meta:
		model = PayConfirm
		exclude = ('owner' , 'assignment', 'date')

class DeliveryConfirmForm(ModelForm):
	class Meta:
		model = DeliveryConfirm
		exclude = ('owner', 'assignment', 'date', )

class PrestigeForm(ModelForm):
	class Meta:
		model = Prestige
		exclude = ('de','to','assignment', 'date', )

