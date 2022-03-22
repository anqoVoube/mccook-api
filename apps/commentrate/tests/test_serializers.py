from django.test import TestCase
from apps.commentrate.serializers.commentrate import RecipeCommentrateSerializer
from rest_framework import serializers


class CommentrateValidationTest(TestCase):
    def test_is_valid_true(self):
        data = {
            "text": "SOMETEXT goes here",
            "rate": 5
        }
        
        serializer_validated = RecipeCommentrateSerializer(data=data)
        self.assertTrue(serializer_validated.is_valid())
    
    def test_is_valid_rate_false(self):
        data = {
            "text": "SOMETEXT goes here",
            "rate": 6
        }
        
        serializer_validated = RecipeCommentrateSerializer(data=data)
        self.assertFalse(serializer_validated.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer_validated.errors, 
                        {
                            "rate_value_error": [
                                "Rate should be between 1 and 5"
                                ]
                        })
    
    def test_is_valid_text_false(self):
        data = {
            "text": "s",
            "rate": 2
        }
        
        serializer_validated = RecipeCommentrateSerializer(data=data)
        self.assertFalse(serializer_validated.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer_validated.errors, 
                        {
                            "text_length": [
                                "Comment must contain at least 3 characters"
                                ]
                        })
    
        
    def test_is_valid_textrate_false(self):
        data = {
            "text": "s",
            "rate": 0
        }
        
        serializer_validated = RecipeCommentrateSerializer(data=data)
        self.assertFalse(serializer_validated.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer_validated.errors, 
                        {
                            "text_length": [
                                "Comment must contain at least 3 characters"
                                ],
                            "rate_value_error": [
                                "Rate should be between 1 and 5"
                                ]
                        })
        
