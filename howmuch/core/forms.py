from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets   
from howmuch.core.models import RequestItem, Proffer, Assignment
from captcha.fields import CaptchaField

class RequestItemForm(ModelForm):
	#captcha = CaptchaField()
	duedate = forms.DateTimeField(widget=widgets.AdminSplitDateTime)
	
	class Meta:
		model = RequestItem
		exclude = ('owner','date','pictures',)

class ProfferForm(ModelForm):
	class Meta:
		model = Proffer
		exclude = ('owner', 'requestItem' ,'date', 'pictures',)

class AssignmentForm(ModelForm):
	duedate = forms.DateTimeField(widget=widgets.AdminSplitDateTime)

	class Meta:
		model = Assignment
		exclude = ('owner', 'requestItem', 'date', 'status', )

