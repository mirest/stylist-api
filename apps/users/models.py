from datetime import datetime, timedelta

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import RegexValidator
from django.db import models

from apps.utils.enums import UserEnum

from .base_model import BaseModel


class UserManager(BaseUserManager, object):

    def create_user(self, password=None):
        if self.phone_number is None:
            raise TypeError('Users must have a phone number.')

        if self.email is None:
            raise TypeError('Users must have an email address.')
        self.verify_user_type()
        self.email = self.normalize_email(self.email)
        self.set_password(password)
        self.is_verified=True
        self.save()
        return self

    def create_superuser(self, password=None):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def verify_user_type(self):
        if self.user_type not in UserEnum.get_user_types():
            values = ' and '.join(UserEnum.get_user_types())
            raise TypeError(f'User type only accepts {values}')


class User(AbstractBaseUser, PermissionsMixin, BaseModel, UserManager, UserEnum):

    email = models.EmailField(unique=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,20}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        db_index=True, unique=True, null=False, blank=False, validators=[phone_regex], max_length=20)

    is_active = models.BooleanField(default=True)

    is_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    user_type = models.CharField(
        max_length=7,
        choices=UserEnum.USER_TYPES,
        default=UserEnum.STYLIST,
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email',)

    def __str__(self):

        return self.email

    @property
    def get_phone_number(self):
        return self.phone_number

    def get_email(self):
        return self.email
