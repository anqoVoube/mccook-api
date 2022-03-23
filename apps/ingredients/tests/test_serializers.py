from django.test import TestCase
from apps.ingredients.serializers.ingredients import IngredientsSerializer

class IngredientsSerializerTest(TestCase):
    def test_capitalized_name(self):
        data = {
            "ingredient_name": "tomato"
        }
        
        serializer = IngredientsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, {
            "ingredient_name": "Tomato"
        })

    def test_none_data(self):
        data = {}
        serializer = IngredientsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("required", serializer.errors.keys())
    