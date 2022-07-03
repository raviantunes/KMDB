from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, is_superuser, is_staff, **other_fields):
        now = timezone.now()

        if not email or not first_name or not last_name:
            raise ValueError("email, first name and last name are mandatory")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_staff=is_staff,
            date_joined=now,
            updated_at=now,
            **other_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, password=None, **other_fields):
        return self._create_user(email, first_name, last_name, password, False, True)

    def create_superuser(self, email, first_name, last_name, password=None, **other_fields):
        return self._create_user(email, first_name, last_name, password, True, True)
