from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import RegexValidator
from django.db import models

from apps.utils.enums import UserEnum

from .base_model import BaseModel


class UserManager(BaseUserManager):

    def create_user(
        self, email=None, phone_number=None, password=None, *args, **kwargs
    ):
        if phone_number is None:
            raise TypeError('Users must have a phone number.')

        if email is None:
            raise TypeError('Users must have an email address.')

        self.verify_user_type(kwargs.get('user_type', 'client'))

        user = self.model(
            phone_number=phone_number, email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_verified = True
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def verify_user_type(self, user_type):
        if user_type not in UserEnum.get_user_types():
            values = ' and '.join(UserEnum.get_user_types())
            raise TypeError(f'User type only accepts {values}')


class User(AbstractBaseUser, PermissionsMixin, BaseModel, UserEnum):

    email = models.EmailField(unique=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,20}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."  # noqa: E501
    )
    phone_number = models.CharField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        validators=[phone_regex],
        max_length=20
    )

    is_active = models.BooleanField(default=True)

    is_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    user_type = models.CharField(
        max_length=7,
        choices=UserEnum.USER_TYPES,
        default=UserEnum.STYLIST,
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email', 'user_type')

    objects = UserManager()

    def __str__(self):

        return self.email

    @property
    def get_phone_number(self):
        return self.phone_number

    def get_email(self):
        return self.email
