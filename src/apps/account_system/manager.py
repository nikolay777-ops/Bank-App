from django.contrib.auth.base_user import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.name = phone_number
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user