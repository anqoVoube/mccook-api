from django.test import TestCase
from apps.recipe.models.recipe import Recipe
from apps.recipe.models.recipe_steps import RecipeSteps
from apps.client.models.client import User, Client


class RecipeModelTest(TestCase):
    def setUp(self):
        self.password = "SomePassword123"
        self.user = User(first_name="Jamoliddin",
                         last_name="Bakhriddinov",
                         username="anqov",
                         email="alex.person7@mail.ru")
        self.user.set_password(self.password)
        self.user.save()
        self.client = Client.objects.get(client_user = self.user)
        self.recipe = Recipe.objects.create(by_cook=self.client,
                              name="Kebab",
                              description="Kebab is delicious meat")
        RecipeSteps.objects.create(step_number=1,
                                   description="FirstStep",
                                   recipe=self.recipe)
        RecipeSteps.objects.create(step_number=2,
                                   description="SecondStep",
                                   recipe=self.recipe)

    def test_recipe_steps_len(self):
        recipe_steps = RecipeSteps.objects.filter(recipe=self.recipe).count()
        recipe_itself = Recipe.objects.all().count()
        self.assertEqual(recipe_steps, 2)
        self.assertEqual(recipe_itself, 1)