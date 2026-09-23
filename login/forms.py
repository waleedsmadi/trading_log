from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label='', help_text='', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username...',
        'id': 'login-username',
    }))

    password = forms.CharField(label='', help_text='', required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password...',
    }))


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise ValidationError('The username should not be empty!')

        if len(username) < 3:
            raise ValidationError('The username should contains at least 3 chars!')
        return username


    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise ValidationError('The password should not be empty!')

        return password


    