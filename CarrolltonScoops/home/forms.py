

from django import forms
from .models import RequestDrive
from django.forms import widgets, FileInput, Textarea
from address.forms import AddressField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MainForm(forms.ModelForm):


	class Meta:
		
		model = RequestDrive
		RequestDrive.destination = AddressField()
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for i in self.fields:

			self.fields[i].widget.attrs['class'] = 'form-control'
		self.fields['destination'].widget.attrs['class'] = 'address pac-target-input form-control'
		self.fields['destination'].widget.attrs['style'] = 'border-top-right-radius: 1rem; border-bottom-right-radius: 1rem;'

		
class RegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for i in self.fields:

			self.fields[i].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['email'].widget.attrs['placeholder'] = 'Email'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'



