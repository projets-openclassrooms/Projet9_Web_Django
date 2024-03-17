from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.TextInput),
    password = forms.CharField(max_length=63, widget=forms.PasswordInput),

class SignupForm(forms.Form):
    password_1 = forms.CharField(max_length=63, widget=forms.PasswordInput),
    password_2 = forms.CharField(max_length=63, widget=forms.PasswordInput),