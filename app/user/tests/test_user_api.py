from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """CREATE AND RETURN A USER"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Reagan'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists(self):
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Reagan'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def password_too_short(self):
        payload = {
            'email': 'test@example.com',
            'password': 'tes',
            'name': 'Reagan'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        userExists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(userExists)