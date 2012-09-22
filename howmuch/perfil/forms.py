from django import forms
from django.forms import ModelForm
from howmuch.perfil.models import Perfil

class PerfilForm(ModelForm):
	class Meta:
		model = Perfil
		exclude = ('user', )