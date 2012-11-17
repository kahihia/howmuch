from django import forms
from django.forms import ModelForm, TextInput
from howmuch.messages.models import Message 

class MessageForm(ModelForm):
	class Meta:
		model = Message
		exclude = ('owner', 'date', 'conversation')
		widgets = {
			'message' : TextInput(attrs={'class':'InputSendMessage','placeholder' : 'Escribe un mensaje aqui...'},),
		}