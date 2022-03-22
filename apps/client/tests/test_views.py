from django.test import TestCase
from apps.client.models.client import Client, User
from apps.commentrate.models.commentrate import CommentRate
from rest_framework.test import APIClient
from django.urls import reverse
import json


class UserCreateView(TestCase):
    pass

class ClientViewTest(TestCase):
    def setUp(self):
        # User
        self.username = "anqov"
        self.email="alex.person7@mail.ru"
        self.password = 'SomePassword123'
        self.user = User(first_name="Jamoliddin",
                         last_name="Bakhriddinov",
                         username=self.username,
                         email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        # Client
        self.client = Client.objects.get(client_user=self.user)
        self.client_id = self.client.id
        
        self.feedbackclient = self.client # For now...
        self.rate = 1
        self.text = "Bad"
        # CommentsRates
        CommentRate.objects.create(by_client=self.feedbackclient,
                                    text=self.text,
                                    rate=self.rate,
                                    to_client=self.client
                                    )
        #Note that rating changes, not when we create CommentRate object,
        # but when we do post request in commentrate of recipe or client.
        self.apiclient = APIClient()
        self.apiclient.force_authenticate(user=self.user)
        self.retrieve_url = reverse('client-retrieve',
                                    kwargs={'pk': self.client_id})
        
    def test_retrieve_client(self):
        request = self.apiclient.get(self.retrieve_url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(json.loads(json.dumps(request.data)), 
              {
                  "client_user": self.username,
                  "rating": 0,
                  "comments_rates": [
                      {
                          "by_client": self.feedbackclient.client_user.username,
                          "rate": self.rate,
                          "text": self.text
                      }
                  ]                  
              })

# !Test for creation of user!