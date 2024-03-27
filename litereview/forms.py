from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from litereview import models
from litereview.models import Ticket, Review
from django import forms


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Nom d'utilisateur :"
        self.fields["password1"].label = "Mot de passe :"
        self.fields["password2"].label = "Confirmer le mot de passe :"

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "email"]


class LogInForm(forms.Form):
    username = forms.CharField(max_length=50, label="Nom d'utilisateur :")
    password = forms.CharField(
        max_length=20, widget=forms.PasswordInput, label="Mot de passe :"
    )


class TicketForm(forms.Form):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-textarea", "placeholder": "Description"}
            ),
            "image": forms.FileInput(attrs={"class": "form-file"}),
        }


class DeleteTicketForm(forms.Form):
    ticket_id = forms.IntegerField(widget=forms.HiddenInput())
    types = forms.CharField(widget=forms.HiddenInput())


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(str(i), "") for i in range(6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "rating-checkbox"}),
    )

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
        widgets = {
            "headline": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "body": forms.Textarea(
                attrs={"class": "form-textarea", "placeholder": "Contenu"}
            ),
        }


class DeleteReviewForm(forms.ModelForm):
    review_id = forms.IntegerField(widget=forms.HiddenInput())
    types = forms.CharField(widget=forms.HiddenInput())


class FollowForm(forms.Form):
    class Meta:
        model = models.UserFollows
        fields = []


class FeedForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = []
