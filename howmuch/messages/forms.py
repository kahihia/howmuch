from django import forms
from django.forms import ModelForm
from howmuch.messages.models import Message 

class MessageForm(ModelForm):
	class Meta:
		model = Message
		exclude = ('owner', 'date', 'conversation')