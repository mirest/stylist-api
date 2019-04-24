from apps.users.models import User


from django.test import TestCase


class TestUserModel(TestCase):

    def test_user_model_saves_data_successfully(self):
        user = User.objects.create_user(
            username='admin',
            email='kimbsimon2@gmail.com',
            phone_number="+1-224-976-4509"
        )
        self.assertIn('id', user.__dict__)
        self.assertEqual('kimbsimon2@gmail.com', user.email)
        self.assertEqual('kimbsimon2@gmail.com', user.get_email())
        self.assertEqual('+1-224-976-4509', user.get_phone_number)

    def test_create_user_without_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username='admin', phone_number="+1-224-976-4509"
            )

    def test_create_user_with_invalid_type(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username='admin',
                email='kimbsimon2@gmail.com',
                phone_number="+1-224-976-4509",
                user_type="erfg"
            )

    def test_create_user_without_phone_number(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username='admin',
                email='kimbsimon2@gmail.com',
                user_type="erfg"
            )

    def test_create_super_user_succeds(self):
        user = User.objects.create_superuser(
            username='admin', email='kimbsimon2@gmail.com', password='wer'
            )
        self.assertIn('id', user.__dict__)
        self.assertEqual(True, user.is_superuser)

    def test_create_super_user_with_no_password_fails(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                username='admin', email='kimbsimon2@gmail.com'
                )
