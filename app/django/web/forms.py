from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm


class AuthenticationForm(BaseAuthenticationForm):
    """
    Add classes to input fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Korisničko ime'})
        self.fields['password'].widget = forms.PasswordInput({'class': 'form-control', 'placeholder': 'Lozinka'})