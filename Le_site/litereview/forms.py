from litereview.models import Ticket, Review
from django import forms


class LoginForm(forms.Form):
    """Collects the requested information to enable an user to log in."""
    username = forms.CharField(max_length=15,
                               label="",
                               widget=forms.TextInput(attrs={
                                   "class": "centered-placeholder",
                                   "placeholder": "Nom d'utilisateur", }))
    password = forms.CharField(max_length=15,
                               label="",
                               widget=forms.PasswordInput(attrs={
                                   "class": "centered-placeholder",
                                   "placeholder": "Mot de passe"}), )
