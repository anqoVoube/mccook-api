from django.test import TestCase
from rest_framework.test import APIClient
from apps.client.models.client import User, Client
from apps.ingredients.models.ingredients import Ingredients
from rest_framework import status
from apps.recipe.models.recipe import Recipe
from apps.recipe.models.recipe_steps import RecipeSteps
from django.urls import reverse
from apps.commentrate.models.commentrate import CommentRate
import json

class RecipeCreateViewTest(TestCase):
    def setUp(self):
        # URL
        self.url = reverse('recipe-create')
        # Ingredients
        self.potato_ing = Ingredients.objects.create(ingredient_name="Potato")
        self.tomato_ing = Ingredients.objects.create(ingredient_name="Tomato")
        self.meat_ing = Ingredients.objects.create(ingredient_name="Meat")
        self.milk_ing = Ingredients.objects.create(ingredient_name="Milk")
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

        self.name = "Kebab"
        self.description = "Kebab is not fried meat, \
but delicious and tasty meal. Your mouth will be watering"
        self.ingredients = ["Potato"]
        self.step_of_recipe = [
            {
                "step_number": 1,
                "description": "FirstStep"
            },
            {
                "step_number": 2,
                "description": "SecondStep"
            }
        ]
        self.apiclient = APIClient()

        self.apiclient.force_authenticate(user=self.user)
    def test_user_assigned_as_bycook(self):
        data = {
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "step_of_recipe": self.step_of_recipe
        }


        response = self.apiclient.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe_count = Recipe.objects.filter(by_cook=self.client).count()
        assert recipe_count == 1
        recipe_fields = Recipe.objects.get(by_cook=self.client)
        self.assertEqual(recipe_fields.name, "Kebab")
    
    def test_ingredients_in_recipe(self):
        data = {
            "name": self.name,
            "description": self.description,
            "ingredients": ['Tomato', 'Potato', 'Meat'],
            "step_of_recipe": self.step_of_recipe
        }

        response = self.apiclient.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(by_cook=self.client)
        all_ingredients = recipe.ingredients.all()
        self.assertTrue(all_ingredients.contains(self.tomato_ing))
        self.assertTrue(all_ingredients.contains(self.potato_ing))
        self.assertTrue(all_ingredients.contains(self.meat_ing))
        self.assertFalse(all_ingredients.contains(self.milk_ing))
    
    def test_recipe_steps(self):
        data = {
            "name": self.name,
            "description": self.description,
            "ingredients": ['Tomato', 'Potato', 'Meat'],
            "step_of_recipe": self.step_of_recipe
        }
        response = self.apiclient.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(by_cook=self.client)
        recipe_steps_first = RecipeSteps.objects\
            .filter(recipe=recipe)\
                .values('step_number', 
                        'description').first()
        self.assertEqual(recipe_steps_first, self.step_of_recipe[0])
        recipe_steps_last = RecipeSteps.objects\
            .filter(recipe=recipe)\
                .values('step_number', 
                        'description').last()
        self.assertEqual(recipe_steps_last, self.step_of_recipe[1])
        recipe_steps_count = RecipeSteps.objects.filter().count()
        self.assertEqual(recipe_steps_count, 2)
    
    def test_incorrect_data(self):
        data = {
            "name": 'w',
            "description": self.description,
            "ingredients": ['Tomato', 'P', 'Med'],
            "step_of_recipe": [
                {
                    "step_number": 1,
                    "description": "SomeDescription"       
                },
                ["good"]
            ]
        }

        response = self.apiclient.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("no_such_ingredient", response.data.keys())
        self.assertIn("incorrect_steps", response.data.keys())
        self.assertIn("len_error_name", response.data.keys())
        self.assertEqual(len(response.data.keys()), 3)

class RecipeListRetrieveViewTest(TestCase):
    def setUp(self):


        #Ingredients
        self.potato_ing = Ingredients.objects.create(ingredient_name="Potato")
        self.tomato_ing = Ingredients.objects.create(ingredient_name="Tomato")
        
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
        
        # Recipe
        self.first_recipe = Recipe.objects.create(name="somename",
                              description="a b c d e f g h j k l q",
                              by_cook=self.client,
                              confirmed="A")
        self.second_recipe = Recipe.objects.create(name="somename2",
                              description="a b c d e f g h j k l q2",
                              by_cook=self.client)
        
        self.first_recipe.ingredients.add(self.potato_ing, self.tomato_ing)
        self.second_recipe.ingredients.add(self.tomato_ing)

        self.first_step = RecipeSteps.objects.create(
            recipe=self.first_recipe,
            step_number=1,
            description="A b d e r t y q w e233e 2 23e23 qds")
        self.second_step = RecipeSteps.objects.create(
            recipe=self.first_recipe,
            step_number=2,
            description="A b d e r t y q we3 w w e 2")

        self.first_recipe_id = self.first_recipe.recipe_id
        # URLS
        self.url_list = reverse('recipe-list')
        self.url_retrieve = reverse('recipe-retrieve',
                                    kwargs={'pk': self.first_recipe_id})
        
        # Comments
        CommentRate.objects.create(by_client=self.client,
                                   text="Very good",
                                   rate=5,
                                   to_recipe=self.first_recipe)
        
        # APIClient
        self.apiclient = APIClient()
        self.apiclient.force_authenticate(user=self.user)

    def test_list_recipe(self):
        response = self.apiclient.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        data_in_str = json.dumps(response.data)
        data_in_dict = json.loads(data_in_str)
        self.assertEqual(len(data_in_dict), 1)
        self.assertEqual(data_in_dict[0]['name'], "somename")
        self.assertIn("name", (data_in_dict[0]).keys())
        self.assertIn("description", (data_in_dict[0]).keys())
        self.assertIn("ingredients", (data_in_dict[0]).keys())
        self.assertNotIn("step_of_recipe", (data_in_dict[0]).keys())

    def test_retrieve_recipe(self):
        response = self.apiclient.get(self.url_retrieve)
        self.assertEqual(response.status_code, 200)
        data_in_str = json.dumps(response.data)
        data_in_dict = json.loads(data_in_str)
        self.assertEqual(data_in_dict, 
            {
                "name": "somename",
                "description": "a b c d e f g h j k l q",
                "ingredients": ["Potato", "Tomato"],
                "step_of_recipe": [
                       {
                          "step_number": 1,
                          "description": "A b d e r t y q w e233e 2 23e23 qds"
                       },
                       {
                          "step_number": 2,
                          "description": "A b d e r t y q we3 w w e 2"
                       },
                ],
                "comments_and_rates": [
                    {
                        "by_client": "anqov",
                        "text": "Very good",
                        "rate": 5
                    }
                ]
            }
        )