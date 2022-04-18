from django.db import models
from django.core.validators import MinLengthValidator


class Recipe(models.Model):
    DECLINE_DELETE = 'D'
    ON_STAGE = 'S'
    ACCEPT_ADD = 'A'
    ACCEPTION_OF_RECIPE = (
        (DECLINE_DELETE, 'Delete'),
        (ON_STAGE, 'On Stage Yet'),
        (ACCEPT_ADD, 'Add'),
    )
    name = models.CharField(max_length=50,
                            validators=[MinLengthValidator(2)])

    description = models.TextField(max_length=400)
    confirmed = models.CharField(
        max_length=2,
        choices=ACCEPTION_OF_RECIPE,
        default=ON_STAGE,
    )
    by_cook = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    ingredients = models.ManyToManyField('ingredients.Ingredients', blank=True)
    client_rated_recipe = models.PositiveIntegerField(default=0, blank=True)
    overall_stars = models.PositiveIntegerField(default=0, blank=True)
    overall_understood = models.PositiveIntegerField(default=0, blank=True)
    clearness_votes = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.name
