from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from litereview import models
from litereview.models import Review, Ticket, UserBlock


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Nom d'utilisateur :"
        self.fields["password1"].label = "Mot de passe :"
        self.fields["password2"].label = "Confirmer le mot de passe :"

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
        help_texts = {
            "username": None,
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
        }
        labels = {
            "username": "",
        }


class LogInForm(forms.Form):
    username = forms.CharField(max_length=50, label="Nom d'utilisateur :")
    password = forms.CharField(
        max_length=20, widget=forms.PasswordInput, label="Mot de passe :"
    )


class TicketForm(forms.ModelForm):
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


class BlockForm:
    class Meta:
        model = UserBlock
        fields = ["blocked_user"]

    def __init__(self):
        self.cleaned_data = None

    def blocked(self):
        pass
