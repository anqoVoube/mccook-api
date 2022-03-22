from django.test import TestCase
from apps.recipe.models.recipe import Recipe
from apps.recipe.models.recipe_steps import RecipeSteps
from apps.client.models.client import Client, User
from apps.ingredients.models.ingredients import Ingredients
from apps.moderator.serializers.moderator import RecipeUpdateSerializer


class ModeratorSerializerTest(TestCase):
    def setUp(self):
        # Class variables
        self.name = "MantiBob"
        self.description = "A B C D E F G H I J K L"
        
        # Ingredients
        Ingredients.objects.bulk_create([
            Ingredients(ingredient_name="Meat"),
            Ingredients(ingredient_name="Onion"),
            Ingredients(ingredient_name="Potato"),
            Ingredients(ingredient_name="Milk")])

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

        # Recipe Steps
        self.first_recipe_step = RecipeSteps.objects.create(step_number=1,
                                                       description="SomeDoc",
                                                       recipe=self.recipe)
        self.second_recipe_step = RecipeSteps.objects.create(step_number=2,
                                                       description="OtherDoc",
                                                       recipe=self.recipe)
    
    def test_update_by_moderator(self):
        data = {
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
        serializer = RecipeUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
