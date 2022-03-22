from django.test import TestCase
from apps.client.models.client import User
from apps.client.serializers.client import UserSerializer
from rest_framework import serializers

class ClientSerializerTest(TestCase):
    def setUp(self):
        # Class Variables
        self.first_name = "Jamoliddin"
        self.last_name = "Bakhriddinov"
        self.username = "anqov"
        self.email = "alex.person7@mail.ru"
        self.password = 'SomePassword123'
        # --------------------------------
        self.user = User(first_name=self.first_name,
                         last_name=self.last_name,
                         username=self.username,
                         email=self.email)
        self.user.set_password(self.password)
        self.user.save()
    
    def test_valid_data(self):
        data = UserSerializer(self.user).data
        assert data['first_name'] == self.first_name
        assert data['last_name'] == self.last_name
        assert data['username'] == self.username
        assert data['email'] == self.email
        assert data['special_question'] is None
        assert data['special_answer'] is None
    
    def test_is_valid_true(self):
        password = "StrongPassword123"
        data = {
            "first_name": "Alex",
            "last_name": "Johnson",
            "username": "alexjohnson7",
            "email": "alexperson@mail.ru",
            "set_password": password,
            "confirm_password": password
        }
        
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_user_exist_error(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "set_password": self.password,
            "confirm_password": self.password,    
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer.errors, {
            "username": ["This username is already taken"],
            "email": ["This email is already taken"]
            })
    
    def test_password_doesnt_match_error(self):
        data = {
            "first_name": "Alex",
            "last_name": "Johnson",
            "username": "alexjohnson7",
            "email": "alexperson@mail.ru",
            "set_password": "FirstPassword",
            "confirm_password": "SecondPassword"
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer.errors, {
            "password": ["Passwords didn't match"]
        })
    
    def test_weak_password_error(self):
        data = {
            "first_name": "Alex",
            "last_name": "Johnson",
            "username": "alexjohnson7",
            "email": "alexperson@mail.ru",
            "set_password": "2",
            "confirm_password": "2"
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer.errors, {
            "min-length": ["Length less than required"],
            "uppercase": ["Password should have at least one uppercase letter"],
            "lowercase": ["Password should have at least one lowercase letter"]
        })
    
    def test_not_valid_email_error(self):
        password = "GoodPassword123"
        data = {
            "first_name": "Alex",
            "last_name": "Johnson",
            "username": "alexjohnson7",
            "email": "alex@ewr",
            "set_password": password,
            "confirm_password": password,
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertIn("invalid-email", serializer.errors.keys())

    def test_first_last_name_error(self):
        password = "GoodPassword123"
        data = {
            "first_name": "alex213",
            "last_name": "bakhri#@#",
            "username": "alexjohnson7",
            "email": "alex2@mail.ru",
            "set_password": password,
            "confirm_password": password,
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer.errors, {
            "fname-error": ["Please provide your real name, so the people \
could find you. This field must have only english letters."],
            "lname-error": ["Please provide your real last name, \
so the people could find you. \
This field must have only english letters."]
        })

    def test_special_question_answer_fields_valid(self):
        password = "GoodPassword123"
        data = {
            "first_name": "alex",
            "last_name": "bakhri",
            "username": "alexjohnson7",
            "email": "alex2@mail.ru",
            "set_password": password,
            "confirm_password": password,
            "special_question": "P",
            "special_answer": "Sobaka"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_special_question_answer_fields_error(self):
        password = "GoodPassword123"
        data = {
            "first_name": "alex",
            "last_name": "bakhri",
            "username": "alexjohnson7",
            "email": "alex2@mail.ru",
            "set_password": password,
            "confirm_password": password,
            "special_answer": "Sobaka"
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(serializers.ValidationError)
        self.assertEqual(serializer.errors, {
            "notwo_null": ["One field was assigned, however second was\'nt."]
        })
    
    def test_capitalized_names_and_answer(self):
        password = "GoodPassword123"
        data = {
            "first_name": "alex",
            "last_name": "bakhri",
            "username": "alexjohnson7",
            "email": "alex2@mail.ru",
            "set_password": password,
            "confirm_password": password,
            "special_question": "P",
            "special_answer": "sobaka"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual("Alex", (serializer.data)["first_name"]),
        self.assertEqual("Bakhri", (serializer.data)["last_name"]),
        self.assertEqual("Sobaka", (serializer.data)["special_answer"]),


                          