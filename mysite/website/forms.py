from django.shortcuts import redirect
from django import forms


class LoginForm(forms.Form):
	email = forms.CharField(max_length=200)
	password = forms.CharField(max_length=200)