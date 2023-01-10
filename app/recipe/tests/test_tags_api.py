from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from core.models import Tag

from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(email='test@example.com', password='Reagan'):
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(tag_id):
    return reverse('recipe:tag-detail', args=[tag_id])


class PublicTagApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        other_user = create_user(email='user@example.com')

        tag = Tag.objects.create(user=self.user, name='Veggie')
        Tag.objects.create(user=other_user, name='Fruity')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    # def test_get_tag_details(self):
    #     tag = Tag.objects.create(user=self.user, name='Veggie')

    #     url = detail_url(tag.id)
    #     res = self.client.get(url)

    #     serializer = TagDetailSerializer(tag)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    def test_update_tag(self):
        tag = Tag.objects.create(user=self.user, name='Veggie')
        payload = {'name': 'New Tag'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])
