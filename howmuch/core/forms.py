# -*- coding: utf-8 -*- 

from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select
from django.contrib.admin import widgets   
from howmuch.core.models import RequestItem, Proffer, Assignment
from captcha.fields import CaptchaField

class NewItemForm1(ModelForm):
	class Meta:
		model = RequestItem
		exclude = {'owner','itemsCatA','itemsCatB','itemsCatC','brand','model','state','date','daysLimit','addressDelivery','pictures'}
		widgets = {
			'price' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. 500'},),
			'title' : TextInput(attrs={'class':'InputFormRequestItem', 'placeholder' : 'Ej. Samsung Galaxy S3 Blanco' }),
            'description': Textarea(attrs={'class':'InputFormRequestItem','cols': 40, 'rows': 10, 'placeholder' : 'Ej. Quiero un Samsung Galaxy S3 de preferencia en color blanco con las siguientes caracteristicas ....'}),
            'quantity' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. 2 ó 3 ó 4'}),
        }

class NewItemForm2(ModelForm):
	class Meta:
		model = RequestItem
		exclude = {'owner','price','title','description','quantity','date','daysLimit','addressDelivery','pictures'}
		widgets = {
            'brand' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. Samsung'}),
            'model' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. Galaxy S3'}),
            'state' : Select(attrs={'class':'InputFormRequestItem',}),
        }


class NewItemForm3(ModelForm):
	class Meta:
		model = RequestItem
		exclude = {'owner','price','title','description','quantity','itemsCatA','itemsCatB','itemsCatC','brand','model','state','pictures'}
		widgets = {
            'daysLimit' : TextInput(attrs={'class':'InputFormRequestItem','placeholder' : 'Ej. 10'}),
            'addressDelivery' : Textarea(attrs={'class':'InputFormRequestItem', 'cols' : 40, 'rows' : '5'}),
        }

class NewItemForm4(forms.Form):
	picture1 = forms.ImageField()
	picture2 = forms.ImageField(required=False)
	picture3 = forms.ImageField(required=False)



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
		widgets = {
			'cprice' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Ej. 500'}),
			'message' : Textarea(attrs={'class' : 'InputFormRequestItem', 'cols': 60, 'rows': 2, 'placeholder' : 'Ej. Debes comprarme el articulo por esta razon, esta otra y esta otra ... '}),
		}


class NewProfferForm1(ModelForm):
	class Meta:
		model = Proffer
		exclude = ('owner', 'requestItem', 'date', 'pictures', )
		widgets = {
			'cprice' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Ej. 500'}),
			'message' : Textarea(attrs={'class' : 'InputFormRequestItem', 'cols' : 60, 'rows' : 2, 'placeholder' : 'Ej. Debes comprarme el articulo por esta razon, esta otra y esta otra ... '}),
		}


class NewProfferForm2(forms.Form):
	picture1 = forms.ImageField()
	picture2 = forms.ImageField(required=False)
	picture3 = forms.ImageField(required=False)


class AssignmentForm(ModelForm):
	duedate = forms.DateTimeField(widget=widgets.AdminSplitDateTime)

	class Meta:
		model = Assignment
		exclude = ('owner', 'requestItem', 'date', 'status', )
		widgets = {
			'comment' : Textarea(attrs={'class' : 'InputFormRequestItem', 'cols' : 60, 'rows' : 10}),
			}

