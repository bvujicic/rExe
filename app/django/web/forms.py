import zipfile

from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from web.models import Algorithm, Iteration


class AuthenticationForm(BaseAuthenticationForm):
    """
    Add classes to input fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Korisničko ime'})
        self.fields['password'].widget = forms.PasswordInput({'class': 'form-control', 'placeholder': 'Lozinka'})


class IterationCreateForm(forms.ModelForm):
    """
    Add classes to input fields.
    """
    class Meta:
        model = Iteration
        fields = ('algorithm', 'input_data')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['algorithm'] = forms.ModelChoiceField(
            queryset=Algorithm.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['input_data'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})

    def clean_input_data(self):
        """
        Try to extract the ZIP file, if it fails return validation error.
        """
        import os
        input_data = self.cleaned_data['input_data']

        try:
            with zipfile.ZipFile(file=input_data.file) as archive:
                # just check if ZIP file is valida
                archive.testzip()

        except zipfile.BadZipFile as exc:
            self.add_error(field='input_data', error=ValidationError(_('neispravna ZIP datoteka')))

        else:
            return input_data

    def save(self, commit=True):
        """
        Relate to currently logged in user.
        """
        self.instance.user = self.user

        return super().save()