from login.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('first_name','last_name','username', 'email', 'password')