from django.urls import re_path
from .views import UserSignUpView, UserLoginView, user_logout

urlpatterns = [
    re_path('^login/', UserLoginView.as_view(), name='login'),
    re_path('^signup/', UserSignUpView.as_view(), name='signup'),
    re_path('^logout/', user_logout, name='logout')
    # re_path('^oauth-login/', name='user-login'),
    # re_path('^oauth/', name='user-oauth'),
]
