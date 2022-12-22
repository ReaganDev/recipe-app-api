"""
TEST FOR MODELS
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import User


class ModelTests(TestCase):
    """TEST MODELS"""

    def test_create_user_with_email_successful(self):
        """test creating a user with email successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(email, password)

        self.assertEqual(user.email, email)
        # self.assertTrue(user.check_password(password))

    # def test_new_user_email_normalized(self):
    #     """test email is normalized"""
    #     sample_emails = [
    #         ['test1@EXAMPLE.com', 'test1@example.com'],
    #         ['Test2@Example.com', 'Test2@example.com'],
    #         ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
    #         ['test4@example.COM', 'test4@example.com'],
    #     ]

    #     for email, expected in sample_emails:
    #         user = get_user_model().objects.create_user(email, 'sample123')
    #         self.assertEqual(user.email, expected)
