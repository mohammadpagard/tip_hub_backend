from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, email=None, fullname=None):
        if not phone_number:
            raise ValueError('User must have an phone number')

        elif not email:
            raise ValueError('User must have an email address')

        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email),
            fullname = fullname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, fullname, password=None):
        user = self.create_user(phone_number, email, fullname, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
