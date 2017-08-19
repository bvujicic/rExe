import zipfile

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm, PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm, UserCreationForm
)
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from web.models import Algorithm, Iteration


User = get_user_model()


class AuthenticationForm(BaseAuthenticationForm):
    """
    Add classes to input fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password'].widget = forms.PasswordInput({'class': 'form-control', 'placeholder': 'Lozinka'})


class PasswordResetForm(BasePasswordResetForm):
    """
    Add classes to input fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Email'})


class SetPasswordForm(BaseSetPasswordForm):
    """
    Add classes to input fields.
    """
    error_messages = {
        'password_mismatch': _('Lozinke ne odgovaraju.'),
    }
    new_password1 = forms.CharField(
        label=_('Lozinka'),
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Lozinka'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('Ponovi lozinku'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Ponovi lozinku'}),
    )


class RegistrationForm(UserCreationForm):
    """
    Add attributes to input fields and email as username/email. Flags user as inactive.
    """
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Ime'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Prezime'})
        self.fields['username'].widget = forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Email (obavezno)'})
        self.fields['password1'].widget = forms.PasswordInput({'class': 'form-control', 'placeholder': 'Lozinka (obavezno)'})
        self.fields['password2'].widget = forms.PasswordInput({'class': 'form-control', 'placeholder': 'Ponovi lozinku (obavezno)'})

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)

        except User.DoesNotExist:
            return username

        else:
            self.add_error(field='username', error=ValidationError(_('Korisnik s navedenom e-mail adresom već postoji.')))

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            is_active=True
        )
        return user


class IterationCreateForm(forms.ModelForm):
    """
    Add classes to input fields.
    Extract input data.
    """
    class Meta:
        model = Iteration
        fields = ('algorithm', 'input_data', 'mail_on_completion')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['algorithm'] = forms.ModelChoiceField(
            queryset=Algorithm.objects.filter(users=self.user),
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['input_data'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})

    def clean_input_data(self):
        """
        Try to extract the ZIP file, if it fails return validation error.
        """
        input_data = self.cleaned_data['input_data']

        try:
            with zipfile.ZipFile(file=input_data.file) as archive:
                # just check if ZIP file is valid
                archive.testzip()

        except zipfile.BadZipFile as exc:
            self.add_error(field='input_data', error=ValidationError(_('Neispravna ZIP datoteka')))

        else:
            return input_data

    def save(self, commit=True):
        """
        Relate to currently logged in user.
        """
        self.instance.user = self.user

        return super().save()