from django import forms
from django.forms import ModelForm, Textarea, TextInput, FileInput, Select

from howmuch.profile.models import Profile, Address, Phone, AccountBank

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'following','addresses', 'phones', 'banks','total_purchases', 'total_sales', 
            'prestige','positive_points','negative_points','unread_notifications', 'unread_conversations')
        widgets = {
            'profile_picture' : FileInput(attrs={'class':'',}),
            'company' : TextInput(attrs={'class':'InputFormRequestItem',}),
        }

class AddressForm(ModelForm):
    class Meta:
        model = Address
        widgets = {
            'street' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Calle'}) ,
            'number' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Numero'}) ,
            'suburb' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Colonia'}) ,
            'city' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Ciudad'}) ,
            'state' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Estado'}) ,
            'country' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Pais'}) ,
            'zipcode' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Codigo Postal'}) ,
        }

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        widgets = {
            'place' : Select(attrs={'class' : 'InputFormRequestItem'}),
            'number' : TextInput(attrs={'class' : 'InputFormRequestItem'}),
        }

class AccountBankForm(ModelForm):
    class Meta:
        model = AccountBank
        widgets = {
            'bank' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Nombre del Banco'}),
            'account' : TextInput(attrs={'class' : 'InputFormRequestItem', 'placeholder' : 'Numero de cuenta'})
        }