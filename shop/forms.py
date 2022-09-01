from django.forms import ModelForm, Textarea, EmailField, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        exclude = ['username']


class AuthenticateUserForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Email Address'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Password'}),
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': "This account is inactive.",
    }


class SellerApplicationForm(ModelForm):
    class Meta:
        model = SellerApplication
        fields = [
            'email',
            'shop_name'
        ]
        widgets = {
            'email': TextInput(attrs={'placeholder': 'Your Email address', 'class': 'input-form', 'required': 'required'}),
            'shop_name': TextInput(attrs={'placeholder': 'Your shop name', 'class': 'input-form', 'required': 'required'})
        }