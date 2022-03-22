from django.test import TestCase
from apps.ingredients.models.ingredients import Ingredients

class IngredientsModelTest(TestCase):
    def setUp(self):
        Ingredients.objects.create(ingredient_name="Potato")
    
    def test_name_capitalize(self):
        ingredient = Ingredients.objects.first()
        self.assertEqual(ingredient.ingredient_name, "Potato")
