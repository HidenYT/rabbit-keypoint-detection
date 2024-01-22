from typing import Any
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_confirm']:
            raise forms.ValidationError("Password confirmation and password differ.")
        return cleaned_data
