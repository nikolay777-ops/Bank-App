from django.contrib import admin
from django import forms

from .models import Contact
from .models.user import User

__all__ = (
    'UserAdmin',
)


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'phone_number', 'password', 'secret_code')
        widgets = {
            'secret_code': forms.PasswordInput(),
            'password': forms.PasswordInput(),
        }


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_user'].queryset = User.objects.all()
        self.fields['to_user'].queryset = User.objects.all()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactAdminForm
    fields = ('from_user', 'to_user', 'is_close')
