from django.test import TestCase
from apps.recipe.models.recipe import Recipe
from apps.recipe.models.recipe_steps import RecipeSteps
from apps.ingredients.models.ingredients import Ingredients
from apps.client.models.client import User, Client
from rest_framework.test import APIClient


class ModeratorViewTest(TestCase):
    def setUp(self):
        # Class variables
        self.name = "MantiBob"
        self.description = "A B C D E F G H I J K L"
        
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
        
        # Recipe
        self.recipe = Recipe.objects.create(name="MantiBob",
                              description="A B C D E F G H I J K L",
                              by_cook=self.client)

        self.recipe.ingredients.add(self.meat_ing, self.tomato_ing)
        self.first_recipe_step = RecipeSteps.objects.create(step_number=1,
                                                       description="SomeDoc",
                                                       recipe=self.recipe)
        self.second_recipe_step = RecipeSteps.objects.create(step_number=2,
                                                       description="OtherDoc",
                                                       recipe=self.recipe)
    def test_update_recipe_and_publish(self):
        data = {
            "confirmed": "A",
            "name": "SomeAnothername",
            "description": "A n o t h e r De sc rip tion",
            "step_of_recipe": [
                {
                    "step_number": 1,
                    "description": "FirstStep"
                },
                {
                    "step_number": 2,
                    "description": "SecondStep"
                }
            ]
        }
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = f'/moderator/{self.recipe.recipe_id}/'
        response = client.patch(url,
                               data,
                               format='json')
        self.assertEqual(response.status_code, 200)

        overall_recipe_steps = RecipeSteps.objects\
            .filter(recipe=self.recipe)\
                .count()
        self.assertEqual(overall_recipe_steps, 2)
        first_recipe_step_updated = RecipeSteps.objects\
            .filter(recipe=self.recipe)\
                .first()
        self.assertEqual(first_recipe_step_updated.description,
                         "FirstStep")
        second_recipe_step_updated = RecipeSteps.objects\
            .filter(recipe=self.recipe)\
                .last()
        self.assertEqual(second_recipe_step_updated.description,
                         "SecondStep")
        recipe = Recipe.objects.get(name="SomeAnothername")
        self.assertEqual(recipe.confirmed, "A")

    def test_update_recipe_and_stage_it(self):
        data = {
            "confirmed": "S",
            "name": "SomeAnothername",
            "description": "A n o t h e r De sc rip tion",
            "step_of_recipe": [
                {
                    "step_number": 1,
                    "description": "FirstStep"
                },
                {
                    "step_number": 2,
                    "description": "SecondStep"
                }
            ]
        }
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = f'/moderator/{self.recipe.recipe_id}/'
        response = client.patch(url,
                               data,
                               format='json')

        self.assertEqual(response.status_code, 200)

        overall_recipe_steps = RecipeSteps.objects\
            .filter(recipe=self.recipe)\
                .count()
        self.assertEqual(overall_recipe_steps, 2)
        first_recipe_step_updated = RecipeSteps.objects\
            .filter(recipe=self.recipe)\
                .first()
        self.assertEqual(first_recipe_step_updated.description,
                         "FirstStep")
        second_recipe_step_updated = RecipeSteps.objects\
            .filter(recipe=self.recipe)\
                .last()
        self.assertEqual(second_recipe_step_updated.description,
                         "SecondStep")
        recipe = Recipe.objects.get(name="SomeAnothername")
        self.assertEqual(recipe.confirmed, "S")
    
    def test_publish_without_changes(self):
        data = {
            "confirmed": "A",
        }
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = f'/moderator/{self.recipe.recipe_id}/'
        response = client.patch(url,
                               data,
                               format='json')

        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(name="MantiBob")
        self.assertEqual(recipe.confirmed, "A")

    def test_stage_recipe_without_changes(self):
        data = {
            "confirmed": "S",
        }
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = f'/moderator/{self.recipe.recipe_id}/'
        response = client.patch(url,
                               data,
                               format='json')

        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(name="MantiBob")
        self.assertEqual(recipe.confirmed, "S")

    def test_delete_recipe(self):
        data = {
            "confirmed": "D",
        }
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = f'/moderator/{self.recipe.recipe_id}/'
        response = client.patch(url,
                               data,
                               format='json')

        self.assertEqual(response.status_code, 204)
        try:
            Recipe.objects.get(name="MantiBob")   # if we will get the object
            # then we will execute the block of code in else statement, 
            # where assert will araise the error.
        except Recipe.DoesNotExist:
            self.assertEqual(1, 1) #passed
        else:
            self.assertEqual("Object was not deleted", "It wasn't removed")
