from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


class Client(models.Model):
    client_user = models.OneToOneField('client.User',
                                       on_delete=models.CASCADE)
    overall_stars = models.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        default=0)

    overall_rated = models.PositiveIntegerField(default=0)
    favorite_recipes = models.ManyToManyField('recipe.Recipe')

    def __str__(self):
        return self.client_user.username
    
class User(AbstractUser):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(
                    special_question__isnull = False, 
                    special_answer__isnull = False
                    ) | Q(
                        special_question = None,
                        special_answer = None
                        ),
                    name = "have_answer_for_question"
            )
        ]

    PET = 'P'
    FIRST_TEACHER = 'T'
    FIRST_JOB = 'J'
    MANUAL_KEY = 'K'
    GRADUATE = 'G'
    QUESTION = [
        (PET, 'Pet name'),
        (FIRST_TEACHER, 'First teacher'),
        (FIRST_JOB, 'First job'),
        (GRADUATE, 'Graduate year from school'),
        (MANUAL_KEY, 'Manual key'),
    ]
    special_question = models.CharField(max_length=40,
                                        choices=QUESTION,
                                        null=True,
                                        blank=True)
    special_answer = models.CharField(max_length=50,
                                      null=True,
                                      blank=True)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Client.objects.create(client_user=self)

    def __str__(self):
        return self.username
