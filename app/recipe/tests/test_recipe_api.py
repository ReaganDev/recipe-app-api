

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from core.models import Recipe
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import (RecipeSerializer, RecipeDetailSerializer)


def create_recipe(user, **params):
    """CREATE AND RETURN A RECIPE"""
    defaults = {
        'title': 'Sample title',
        'description': 'Sample description',
        'price': Decimal('4.5'),
        'time_minutes': 25,
        'link': 'http:/example.com/recipe'
    }

    defaults.update(**params)
    return Recipe.objects.create(user=user, **defaults)


def create_user(**params):
    return get_user_model().objects.create_user(**params)


RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


class PublicRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        other_user = create_user(email='other@example.com', password='Reagan')

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_details(self):
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        payload = {
            'title': 'Sample title',
            'price': Decimal('4.5'),
            'time_minutes': 25,
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        original_link = 'http://google.com/pdf'
        recipe = create_recipe(
            title='Sample title',
            link=original_link,
            user=self.user
        )
        payload = {'title': 'New Title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)

    def test_cannot_update_user(self):
        recipe = create_recipe(user=self.user)
        new_user = create_user(email='other@example.com', password='Reagan')
        payload = {'user': new_user.id}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
