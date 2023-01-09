"""
TEST FOR MODELS
"""
from decimal import Decimal
from core import models
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import User


def create_user(email='user@example.com', password='Reagan'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """TEST MODELS"""

    def test_create_user_with_email_successful(self):
        """test creating a user with email successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(email=email, password=password,)

        # self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test email is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """Creating a user without an email raises a value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """test creating a superuser"""
        user = get_user_model().objects.create_superuser('test@example.com', 'test123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            'test@example.com', 'test123')

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe',
            time_minutes=25,
            price=Decimal('3.5'),
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag 1')

        self.assertEqual(str(tag), tag.name)
