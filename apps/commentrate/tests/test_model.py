from django.test import TestCase
from apps.commentrate.models.commentrate import CommentRate
from apps.client.models.client import Client, User
from apps.recipe.models.recipe import Recipe


class CommentrateModelTest(TestCase):
    def setUp(self):
        # First User(who rates)
        self.password = 'SomePassword123'
        self.user_rates = User(first_name="Jamoliddin",
                         last_name="Bakhriddinov",
                         username="anqov",
                         email="alex.person7@mail.ru")
        self.user_rates.set_password(self.password)
        self.user_rates.save()
        self.client_rates = Client.objects.get(client_user=self.user_rates)
        
        # Second User(who receive the rate)
        self.password = 'SomePassword123'
        self.user_receiver = User(first_name="Jamoliddin",
                         last_name="Bakhriddinov",
                         username="anqov2",
                         email="alex.person2@mail.ru")
        self.user_receiver.set_password(self.password)
        self.user_receiver.save()
        self.client_receiver = Client.objects.get(
            client_user=self.user_receiver)
        self.commentrate = CommentRate.objects.create(
                                            by_client=self.client_rates,
                                            text="Something good and not bad",
                                            rate=5,
                                            to_client=self.client_receiver)
        self.recipe = Recipe.objects.create(
                                    by_cook=self.client_receiver,
                                    name="Poetry",
                                    description="A B C D E F G H I K L M N")
    
    def test_creation_of_comment_and_rate(self):
        count_queryset = CommentRate.objects.all().count()
        self.assertEqual(count_queryset, 1)
    
    def test_multiple_destinations(self):
        '''Rate client and recipe at the same time(should raise an error)'''
        try:
            CommentRate.objects.create(by_client=self.client_rates,
                                   text="Something good and not bad",
                                   rate=5,
                                   to_client=self.client_receiver,
                                   to_recipe=self.recipe)
        except:
            self.assertEqual(1, 1) # passed
        else:
            self.assertEqual('The object was created', 'Too bad') # didnt pass
    
    def test_rate_min_max_values(self):
        '''Checking whether not valid rate can bypass the validators'''
        instance = CommentRate.objects.create(by_client=self.client_rates,
                                   text="Something good and not bad",
                                   rate=100,
                                   to_client=self.client_receiver)
        try:
            instance.full_clean()
        except:
            self.assertEqual(1, 1) # passed
        else:
            self.assertEqual('The object was created', 'Too bad') # didnt pass
