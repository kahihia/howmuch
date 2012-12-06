from django import forms
from django.forms import ModelForm
from howmuch.Profile.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )