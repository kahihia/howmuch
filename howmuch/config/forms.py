from django import forms
from django.forms import ModelForm
from howmuch.config.models import NotificationsConfig

class NotificationsConfigForm(ModelForm):
	class Meta:
		model = NotificationsConfig
		exclude = {'user',}
