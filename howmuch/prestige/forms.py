from django import forms
from django.forms import ModelForm
from howmuch.prestige.models import PayConfirm, DeliveryConfirm, PrestigeLikeBuyer, PrestigeLikeSeller

class PayConfirmForm(ModelForm):
	class Meta:
		model = PayConfirm
		exclude = ('owner' , 'assignment', 'date')

class DeliveryConfirmForm(ModelForm):
	class Meta:
		model = DeliveryConfirm
		exclude = ('owner', 'assignment', 'date', )

class PrestigeLikeBuyerForm(ModelForm):
	class Meta:
		model = PrestigeLikeBuyer
		exclude = ('de', 'to', 'assignment', 'date', )

class PrestigeLikeSellerForm(ModelForm):
	class Meta:
		model = PrestigeLikeSeller
		exclude = ('de', 'to', 'assignment', 'date')

