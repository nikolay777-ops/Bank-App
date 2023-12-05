from django.contrib import admin
from django import forms

from .models.user import User

__all__ = (
    'UserAdmin',
)


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'otp_code': forms.PasswordInput()
        }


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

