from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, label='Username')
    password = forms.CharField(max_length=255, label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise ValidationError('Both username and password are required')

        return self.cleaned_data