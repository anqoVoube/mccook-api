from django.test import TestCase
from apps.client.models.client import Client, User
from apps.recipe.models.recipe import Recipe
from rest_framework.test import APIClient


class CommentrateViewTest(TestCase):
    def setUp(self):
        # User
        self.password = 'SomePassword123'
        self.user = User(first_name="Jamoliddin",
                         last_name="Bakhriddinov",
                         username="anqov",
                         email="alex.person7@mail.ru")
        self.user.set_password(self.password)
        self.user.save()
        # Client
        self.client = Client.objects.get(client_user=self.user)
        self.recipe = Recipe.objects.create(
                            name="somename",
                            description="a b c d e r t y u i o",
                            by_cook=self.client)
        self.recipe_id = int(self.recipe.recipe_id)# <---- by client who rates!!!
        self.client_id = self.client.id
        print("ID", self.recipe_id)
    def test_recipe_rate(self):
        data = {
            "text": "someteqwext",
            "rate": 3,
            "understandable": False
        }
        client = APIClient()
        client.login(username="anqov", password="SomePassword123")
        url = f'/recipe/{self.recipe_id}/coraun/'
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(pk=self.recipe_id)
        self.assertEqual(recipe.overall_stars, 3)
        self.assertEqual(recipe.client_rated_recipe, 1)
        self.assertEqual(recipe.overall_understood, 0)
        self.assertEqual(recipe.clearness_votes, 1)
    
    def test_client_rate(self):
        data = {
            "text": "sometexqwet",
            "rate": 5,
        }
        client = APIClient()
        client.login(username="anqov", password="SomePassword123")
        url = f'/client/{self.client_id}/coraun/'
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)        
        client = Client.objects.get(pk=self.client_id)
        self.assertEqual(client.overall_stars, 5)
        self.assertEqual(client.overall_rated, 1)


