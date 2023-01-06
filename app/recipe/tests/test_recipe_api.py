

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from core.models import Recipe
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import RecipeSerializer


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
    return Recipe.objects.create(user, **defaults)


RECIPE_URL = 'recipe:recipes'


class PublicRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        email = 'test@example.com'
        password = 'testpass123'
        self.user = get_user_model().objects.create_user(email=email, password=password)
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
        other_user = get_user_model().objects.create_user('other@example.com', 'Reagan')

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
