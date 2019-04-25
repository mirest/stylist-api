import factory
from apps.users.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')
    is_verified = True
    user_type = 'client'


class AdminFactory(UserFactory):
    is_staff = True
