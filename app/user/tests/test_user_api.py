from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_USER_URL = reverse('user:login')
ME_URL = reverse('user:me')


def create_user(**params):
    """CREATE AND RETURN A USER"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Unauthenticated tests"""

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
        self.assertTrue(user.check_password(payload['password']))
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

    def test_create_user_token(self):
        user_details = {
            'email': 'test@example.com',
            'password': 'tes',
            'name': 'Reagan'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_wrong_password(self):
        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com', 'password': 'badpass'}

        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com', 'password': ''}

        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Authenticated tests"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='test123',
            name='Reagan',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_not_allowed(self):

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):

        payload = {
            'name': 'Nonso',
            'password': 'Reagan12'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password, payload['password'])
