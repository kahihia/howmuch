from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _


from howmuch.config.models import Notifications

class NotificationsConfigForm(ModelForm):
    class Meta:
        model = Notifications
        exclude = {'user',}


class EmailChangeForm(forms.Form):
	"""
	Formulario que le permite al usuario cambiar su correo electronico
	si coincide su password
	"""

	error_messages = {
		'incorrect_password' : _("The Password is incorrect")
	}

	new_email = forms.EmailField(label=_("new email"))
	password = forms.CharField(label=_("current password"),
								widget=forms.PasswordInput)

	def __init__(self,user,*args,**kwargs):
		self.user = user
		super(EmailChangeForm, self).__init__(*args, **kwargs)

	def clean_password(self):
		if not self.user.check_password(self.cleaned_data['password']):
			raise forms.ValidationError(
				self.error_messages['incorrect_password'])


	def save(self, commit=True):
		self.user.check_password(self.cleaned_data['password'])
		if commit:
			self.user.email = self.cleaned_data['new_email']
			self.user.save()
		return self.user






