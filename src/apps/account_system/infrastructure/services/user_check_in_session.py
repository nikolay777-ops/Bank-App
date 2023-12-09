from django.core.cache import cache
from account_system.models import User
from django.http import HttpRequest

def user_check_in_session(request: HttpRequest, cache: cache):
    user_id = request.session.get('user_id')
    user_name = cache.get(f'user_name')

    try:
        user = User.objects.get(id=user_id, name=user_name)
    except User.DoesNotExist:
        return False
    return user