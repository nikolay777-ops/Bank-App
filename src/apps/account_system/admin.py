from django.contrib import admin
from django import forms

from account_system.models import User, Role, Permission, Account, RolesPermissions


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserViewAdmin(admin.ModelAdmin):
    form = UserAdminForm

class RoleAdminForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'


@admin.register(Role)
class RoleViewAdmin(admin.ModelAdmin):
    form = RoleAdminForm

class PermissionAdminForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'


@admin.register(Permission)
class PermissionViewAdmin(admin.ModelAdmin):
    form = PermissionAdminForm

class AccountAdminForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


@admin.register(Account)
class AccountViewAdmin(admin.ModelAdmin):
    form = AccountAdminForm

class RolesPermissionsAdminForm(forms.ModelForm):
    class Meta:
        model = RolesPermissions
        fields = '__all__'


@admin.register(RolesPermissions)
class RolesPermissionsViewAdmin(admin.ModelAdmin):
    form = RolesPermissionsAdminForm