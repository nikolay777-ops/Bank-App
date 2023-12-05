from django import forms

__all__ = (
    'LoginForm'
)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
