from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select
from django.contrib.admin import widgets   
from howmuch.core.models import RequestItem, Proffer, Assignment
from captcha.fields import CaptchaField

class RequestItemForm(ModelForm):
	#captcha = CaptchaField()	
	class Meta:
		model = RequestItem
		exclude = ('owner','date','pictures',)
		widgets = {
			'price' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. 500'}),
			'title' : TextInput(attrs={'class':'InputFormRequestItem', 'placeholder' : 'Ej. Samsung Galaxy S3 Blanco' }),
            'description': Textarea(attrs={'class':'InputFormRequestItem','cols': 40, 'rows': 10}),
            'quantity' : TextInput(attrs={'class':'InputFormRequestItem',}),
            'brand' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. Samsung'}),
            'model' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. Galaxy S3'}),
            'state' : Select(attrs={'class':'InputFormRequestItem',}),
            'daysLimit' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. 10'}),
            'addressDelivery' : Textarea(attrs={'class':'InputFormRequestItem', 'cols' : 40, 'rows' : '5'}),
        }

class ProfferForm(ModelForm):
	class Meta:
		model = Proffer
		exclude = ('owner', 'requestItem' ,'date', 'pictures',)

class AssignmentForm(ModelForm):
	duedate = forms.DateTimeField(widget=widgets.AdminSplitDateTime)

	class Meta:
		model = Assignment
		exclude = ('owner', 'requestItem', 'date', 'status', )

