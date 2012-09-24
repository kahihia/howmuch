from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets   
from howmuch.core.models import RequestItem, Proffer

class RequestItemForm(ModelForm):
	duedate = forms.DateTimeField(widget=widgets.AdminSplitDateTime)
	
	class Meta:
		model = RequestItem
		exclude = ('owner','date','pictures',)

class ProfferForm(ModelForm):
	class Meta:
		model = Proffer
		exclude = ('owner', 'requestItem' ,'date', 'pictures',)
