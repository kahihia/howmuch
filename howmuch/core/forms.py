# -*- coding: utf-8 -*- 

from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select, ModelChoiceField
from django.contrib.admin import widgets   
from howmuch.core.models import RequestItem, Proffer, Assignment
from howmuch.perfil.models import Address
from captcha.fields import CaptchaField

class NewItemForm1(ModelForm):
    class Meta:
        model = RequestItem
        fields = {'title'}
        widgets = {
            'title' : TextInput(attrs={'class' : 'InputFormRequestItemNew', 'placeholder' : 'Ej. iPhone 5 32 Gb Color Blanco en Buen Estado'}, ),
        }

class NewItemForm2(ModelForm):
    class Meta:
        model = RequestItem
        fields = {'price'}
        widgets = {
            'price' : TextInput(attrs={'class':'InputFormRequestItemNew','placeholder' : 'Ej. 10000.00'},),
        }

class NewItemForm3(ModelForm):
    class Meta:
        model = RequestItem
        fields = {'quantity'}
        widgets = {
            'quantity' : TextInput(attrs={'class':'InputFormRequestItemNew','placeholder' : 'Ej. 2'}, ),
        }

class NewItemForm4(ModelForm):
    class Meta:
        model = RequestItem
        fields = {'description'}
        widgets = {
             'description': Textarea(attrs={'class':'InputFormRequestItemNew','cols': 40, 'rows': 10, 'placeholder' : 'Describe tu producto Aqui'}),
        }

class NewItemForm5(ModelForm):
    class Meta:
        model = RequestItem
        fields = {'itemsCatA','itemsCatB','itemsCatC','brand','model','state'}
        widgets = {
            'brand' : TextInput(attrs={'class':'InputFormRequestItemNew','placeholder' : 'Ej. Samsung'}),
            'model' : TextInput(attrs={'class':'InputFormRequestItemNew','placeholder' : 'Ej. Galaxy S3'}),
            'state' : Select(attrs={'class':'InputFormRequestItemNew',}),
        }

class NewItemForm6(ModelForm):
    class Meta:
        model = RequestItem
        fields = {'daysLimit','addressDelivery'}
        widgets = {
            'daysLimit' : Select(attrs={'class':'InputFormRequestItemNew',}),
            'addressDelivery' : Select(attrs={'class':'InputFormRequestItemNew'}),
        }

class NewItemForm7(forms.Form):
    picture1 = forms.ImageField()
    picture2 = forms.ImageField(required=False)
    picture3 = forms.ImageField(required=False)
    picture4 = forms.ImageField(required=False)
    picture5 = forms.ImageField(required=False)

class ProfferForm(forms.Form):
    cprice = forms.IntegerField(
        widget = forms.TextInput(attrs = {'class' : 'InputForm'}))
    message = forms.CharField(
        widget = forms.Textarea(attrs = {'class' : 'InputForm TextareaForm'}))
    picture1 = forms.ImageField(
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image1')"}))
    picture2 = forms.ImageField(required=False,
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image2')"}))
    picture3 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image3')"}))
    picture4 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image4')"}))
    picture5 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image5')"}))

class AssignmentForm(ModelForm):
    
    class Meta:
        model = Assignment
        exclude = ('owner', 'requestItem', 'date', 'status', )
        widgets = {
            'comment' : Textarea(attrs={'class' : 'InputForm TextareaForm', 'cols' : 60, 'rows' : 10}),
            }

