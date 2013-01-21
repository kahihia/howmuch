from django import forms
from django.forms import ModelForm

from howmuch.config.models import Notifications

class NotificationsConfigForm(ModelForm):
    class Meta:
        model = Notifications
        exclude = {'user',}
