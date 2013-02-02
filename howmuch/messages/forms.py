from django import forms
from django.forms import ModelForm, Textarea
from howmuch.messages.models import Message 

class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('owner', 'date', 'conversation')
        widgets = {
            'message' : Textarea(attrs={'class' : 'span6', 'rows' : 2,'placeholder' : 'Escribe un mensaje aqui...'}),
        }