from django import forms
from django.core.validators import RegexValidator

__all__ = (
    'LoginForm',
)

class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=13,
        validators=[RegexValidator(
            r'^\+375\d{9}$',
            'Phone number must be in the format: +375 followed by 9 digits and start with 375'
        ), ]
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

    field_order = ['phone_number', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].label = 'Phone Number'

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password1 = cleaned_data.get('password1')

        if phone_number and password1:
            # Perform additional validation if needed
            pass

        return cleaned_data