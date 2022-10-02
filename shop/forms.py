from django.forms import ModelForm, Textarea, EmailField, TextInput, CheckboxInput, NumberInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django import forms


class CreateUserForm(UserCreationForm):

    registration_code = forms.CharField(
        label='registration_code',
        widget=forms.TextInput(attrs={'placeholder': 'Your registration code', 'class': 'input-form', 'required': 'required'})
    )
    design_requests = forms.CharField(
        label='design_requests',
        widget=forms.Textarea(attrs={'placeholder': 'How do you want your website to look?', 'class': '', 'required': 'required'})
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        exclude = ['username']

        widgets = {
            'email': TextInput(
                attrs={'placeholder': 'Your Email address', 'class': 'input-form', 'required': 'required'}),
            'password': forms.PasswordInput(
                attrs={'autocomplete': 'current-password', 'placeholder': 'Password'}
            ),
            'first_name': TextInput(
                attrs={'placeholder': 'First Name', 'class': 'input-form', 'required': 'required'}
            ),
            'last_name': TextInput(
                attrs={'placeholder': 'Last Name', 'class': 'input-form', 'required': 'required'}
            ),
        }


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


class HelpMessageForm(ModelForm):
    class Meta:
        model = HelpMessage
        fields = [
            'email',
            'message'
        ]
        widgets = {
            'email': TextInput(attrs={'placeholder': 'Your Email address', 'class': 'input-form', 'required': 'required'}),
            'message': Textarea(attrs={'placeholder': 'Your message', 'class': 'input-form', 'required': 'required'})
        }


class NewsletterEmailForm(ModelForm):
    class Meta:
        model = NewsletterEmail
        fields = [
            'email',
        ]
        widgets = {
            'email': TextInput(attrs={'placeholder': 'Your Email address', 'class': 'input-form', 'required': 'required'}),
        }


class PoliciesForm(ModelForm):
    class Meta:
        model = SellerPolicies
        fields = [
            'shipping_general_information',
            'shipping_customs_and_taxes',
            'accepts_returns',
            'accepts_exchanges',
            'accepts_cancellations',
            'contact_within',
            'ship_back_within',
            'request_cancellation',
            'returns_conditions',
            'returns_questions',
            'privacy'
        ]
        widgets = {
            'shipping_general_information': Textarea(
                attrs={'placeholder': 'General Information', 'class': 'block1-inputfield', 'onkeydown': 'showSaveButton()'}),
            'shipping_customs_and_taxes': Textarea(
                attrs={'placeholder': 'Customs and Import Taxes', 'class': 'block1-inputfield', 'onkeydown': 'showSaveButton()'}),
            'returns_conditions': Textarea(
                attrs={'placeholder': 'Conditions of Returns', 'class': 'block1-inputfield', 'onkeydown': 'showSaveButton()'}),
            'returns_questions': Textarea(
                attrs={'placeholder': 'Questions about your Order?', 'class': 'block1-inputfield', 'onkeydown': 'showSaveButton()'}),
            'privacy': Textarea(
                attrs={'placeholder': 'Privacy Policy', 'class': 'block3-inputfield', 'onkeydown': 'showSaveButton()'}),

            'accepts_returns': CheckboxInput(
                attrs={'onchange': 'showSaveButton()'}),
            'accepts_exchanges': CheckboxInput(
                attrs={'onchange': 'showSaveButton()'}),
            'accepts_cancellations': CheckboxInput(
                attrs={'onchange': 'showSaveButton()'}),

            'contact_within': NumberInput(
                attrs={'min': 0, 'max': 300, 'id': 'exchange-input', 'onfocus': 'showSaveButton()'}),
            'ship_back_within': NumberInput(
                attrs={'min': 0, 'max': 300,  'id': 'returns-input', 'onfocus': 'showSaveButton()'}),
            'request_cancellation': TextInput(
                attrs={'placeholder': 'when should you be contacted?', 'id': 'cancellation-input', 'onkeydown': 'showSaveButton()'}),

        }
