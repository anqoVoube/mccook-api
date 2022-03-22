from django.test import TestCase
from apps.client.models.client import User, Client

class ClientModelTest(TestCase):
    def setUp(self):
        self.password = 'SomePassword123'
        self.user = User(first_name="Jamoliddin",
                         last_name="Bakhriddinov",
                         username="anqov",
                         email="alex.person7@mail.ru")
        self.user.set_password(self.password)
        self.user.save()

    def test_created_model(self):
        get_user = User.objects.get(username="anqov")
        self.assertIsNone(get_user.special_question)
        self.assertIsNone(get_user.special_answer)
        self.assertEqual(get_user, self.user)
        self.assertTrue(get_user.check_password(self.password))
    
    def test_client_model(self):
        get_client = Client.objects.get(client_user=self.user)
        self.assertEqual(get_client.overall_stars, 0)
        self.assertEqual(get_client.overall_rated, 0)
        