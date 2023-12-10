from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            if 'username' in kwargs:
                phone_number = kwargs['username']

            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            errors = {
                'phone_number': [
                    'User with this phone number does not exist'
                ]
            }
            return errors

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
