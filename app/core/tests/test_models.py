"""
TEST FOR MODELS
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """TEST MODELS"""

    def test_create_user_with_email_successful(self):
        """test creating a user with email successful"""
        email = 'test@example.com'
        password = 'test@123'
        user = get_user_model().objects.create(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
