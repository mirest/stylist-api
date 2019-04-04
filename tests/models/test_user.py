from django.test import TestCase

from apps.users.models import User

from ..factories.users import UserFactory


class TestUserModel(TestCase):
    
    def test_user_model_saves_data_successfully(self):

        user=UserFactory(email="kimbsimon2@gmail.com",phone_number='+1-224-976-4509')
        user.create_user()
        self.assertIn('id',user.__dict__)
        self.assertEqual('kimbsimon2@gmail.com',user.email)
        self.assertEqual('kimbsimon2@gmail.com',user.get_email())
        self.assertEqual('+1-224-976-4509',user.get_phone_number)
    
    def test_create_user_without_email(self):
        user=UserFactory(email=None)
        with self.assertRaises(TypeError):
            user.create_user()
    
    def test_create_user_without_phone_number(self):
        user=UserFactory(phone_number=None)
        with self.assertRaises(TypeError):
            user.create_user()
    
    def test_create_super_user_succeds(self):
        user=UserFactory(phone_number='+1-224-976-4509')
        user.create_superuser(password="qwertrewqert")
        self.assertIn('id',user.__dict__)
        self.assertEqual(True, user.is_superuser)

    def test_create_super_user_with_no_password_fails(self):
        user=UserFactory()
        with self.assertRaises(TypeError):
            user.create_superuser()
