from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Custom user-manager with checking of phone-number"""
    use_in_migrations = True

    def create_user(self, phone=None, username=None, email=None, password=None, **extra_fields):
        if not phone and not username:
            raise ValueError('Users must have a phone or username')
        username = phone

        user = self.model(
            username=username,
            email=email,
            phone=phone,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, phone=None, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user
