from django import forms
from django.forms import ModelForm, Textarea, TextInput, FileInput, Select

from howmuch.profile.models import Profile, Address, Phone, AccountBank

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','is_new','is_his_first_post','following','addresses', 'phones', 'banks','total_purchases', 'total_sales', 
            'prestige','positive_points','negative_points','unread_notifications', 'unread_conversations',
            'current_invoice', 'credit_limit','is_block')
        widgets = {
            'profile_picture' : FileInput(attrs={'class':'text password width-100',}),
            'company' : TextInput(attrs={'class':'text width-100',}),
        }

class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('owner',)
        widgets = {
            'street' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Calle'}) ,
            'number' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Numero'}) ,
            'suburb' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Colonia'}) ,
            'city' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Ciudad'}) ,
            'state' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Estado'}) ,
            'country' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Pais'}) ,
            'zipcode' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Codigo Postal'}) ,
        }

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        exclude = ('owner', )
        widgets = {
            'place' : Select(attrs={'class' : 'span12'}),
            'number' : TextInput(attrs={'class' : 'span12'}),
        }

class AccountBankForm(ModelForm):
    class Meta:
        model = AccountBank
        exclude = ('owner', )
        widgets = {
            'bank' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Nombre del Banco'}),
            'account' : TextInput(attrs={'class' : 'span12', 'placeholder' : 'Numero de cuenta'})
        }