from django.test import TestCase
from apps.ingredients.models.ingredients import Ingredients
from apps.client.models.client import User, Client
from apps.recipe.serializers.recipe import RecipeCreateSerializer
from rest_framework import serializers


class RecipeSerializerTest(TestCase):
    def setUp(self):
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
        self.name = "Kebab"
        self.description = "Kebab is not fried meat, \
but delicious and tasty meal. Your mouth will be watering"
        self.ingredients = ["Meat", "Onion", "Potato"]
        self.step_of_recipe = [
            {
                "step_number": 1,
                "description": "good"
            },
            {
                "step_number": 2,
                "description": "too good"
            },
            {
                "step_number": 3,
                "description": "tuple good"
            }    
        ]

    def test_is_valid_true(self):
        data = {
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "step_of_recipe": self.step_of_recipe,
        }
        
        serializer = RecipeCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_name_error(self):
        # Name-Length issues test (len(name) < 2)
        length_name_data = {
            "name": '',
            "description": self.description,
            "ingredients": self.ingredients,
            "step_of_recipe": self.step_of_recipe,
        }
        length_name_serializer = RecipeCreateSerializer(data=length_name_data)
        self.assertFalse(length_name_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(length_name_serializer.errors, {
            "len_error_name": ["name object must have at least 2 letters"]
        })
        
        # Name not assigned (name is None)
        none_name_data = {
            "description": self.description,
            "ingredients": self.ingredients,
            "step_of_recipe": self.step_of_recipe,
        }
        none_name_serializer = RecipeCreateSerializer(data=none_name_data)
        self.assertFalse(none_name_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(none_name_serializer.errors, {
            "not_assigned_name": ["name object is not assigned"]
        })

    def test_description_error(self):
        # Description-min-word issues test (words < 10)
        min_word_data = {
            "name": self.name,
            "description": "Not enough words",
            "ingredients": self.ingredients,
            "step_of_recipe": self.step_of_recipe,
        }
        min_word_serializer = RecipeCreateSerializer(
            data=min_word_data
            )
        self.assertFalse(min_word_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(min_word_serializer.errors, {
            "min_word_description": [
                "description object must have at least 10 words"
                ]
        })

        # Description is not assigned (description is None)
        none_description_data = {
            "name": self.name,
            "ingredients": self.ingredients,
            "step_of_recipe": self.step_of_recipe,
        }
        none_description_serializer = RecipeCreateSerializer(
            data=none_description_data
            )
        self.assertFalse(none_description_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(none_description_serializer.errors, {
            "not_assigned_description": ["description object is not assigned"]
        })

    def test_ingredients_error(self):
        # Empty ingredients test (ingredients = [])
        empty_ingredients_data = {
            "name": self.name,
            "description": self.description,
            "ingredients": [],
            "step_of_recipe": self.step_of_recipe,
        }
        empty_ingredients_serializer = RecipeCreateSerializer(
            data=empty_ingredients_data
            )
        self.assertFalse(empty_ingredients_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(empty_ingredients_serializer.errors, {
            "empty_list_ingredients": [
                "ingredients list can\'t be empty"
                ]
        })

        # ingredients-list is not assigned (ingredients is None)
        none_ingredients_data = {
            "name": self.name,
            "description": self.description,
            "step_of_recipe": self.step_of_recipe,
        }
        none_ingredients_serializer = RecipeCreateSerializer(
            data=none_ingredients_data
            )
        self.assertFalse(none_ingredients_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(none_ingredients_serializer.errors, {
            "not_assigned_ingredients": ["ingredients object is not assigned"]
        })

    def test_steps_error(self):
        # Empty steps-list test (ingredients = [])
        empty_steps_data = {
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "step_of_recipe": [],
        }
        empty_steps_serializer = RecipeCreateSerializer(
            data=empty_steps_data
            )
        self.assertFalse(empty_steps_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(empty_steps_serializer.errors, {
            "empty_list_steps": [
                "steps list can\'t be empty"
                ]
        })

        # Steps are not assigned (step_of_recipe is None)
        none_steps_data = {
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
        }
        none_steps_serializer = RecipeCreateSerializer(
            data=none_steps_data
            )
        self.assertFalse(none_steps_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(none_steps_serializer.errors, {
            "not_assigned_steps": ["steps object is not assigned"]
        })
    
    def test_fields_error(self):
        wrong_data = {
            "name": 'w',
            "description": 'Bad description',
        }
        
        wrong_data_serializer = RecipeCreateSerializer(data=wrong_data)
        self.assertFalse(wrong_data_serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(wrong_data_serializer.errors, {
            "len_error_name": ["name object must have at least 2 letters"],
            "min_word_description": [
                "description object must have at least 10 words"
                ],
            "not_assigned_ingredients": [
                "ingredients object is not assigned"
                ],
            "not_assigned_steps": [
                "steps object is not assigned"
                ]
        })