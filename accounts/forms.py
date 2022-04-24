from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer

class CreateUserForm(UserCreationForm):
	class Meta:
		model = Customer
		fields = ['username', 'email', 'password1', 'password2']

