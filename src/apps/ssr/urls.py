from django.urls import re_path, include
from .user.urls import urlpatterns as user_url_patterns

urlpatterns = [
    re_path('^', include(user_url_patterns))
]
