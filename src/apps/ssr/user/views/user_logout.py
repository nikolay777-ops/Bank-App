from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import viewsets, permissions

# TODO: check which type of request is logout and define using viewset methods

__all__ = (
    'UserLogoutViewSet',
    'user_logout',
)


class UserLogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]


def user_logout(request):
    logout(request)
    return redirect('login')
