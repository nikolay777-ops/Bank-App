from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from ..models import User

__all__ = (
    'RegistrationForm',
)


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=13,
        validators=[RegexValidator(
            r'^\+375\d{9}$',
            'Phone number must be in the format: +375 followed by 9 digits and start with 375'
        ),]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Username'
        self.fields['phone_number'].label = 'Phone Number'