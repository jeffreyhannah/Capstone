from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import uploadFile


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class uploadForm(forms.ModelForm):
    class Meta:
        model = uploadFile
        fields = ['user','file_field']
        #widgets = {'user': forms.HiddenInput()}


