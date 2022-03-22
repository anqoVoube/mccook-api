from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RecipeSteps(models.Model):
    step_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)]
        )

    description = models.CharField(max_length=200)
    recipe = models.ForeignKey('recipe.Recipe',
                               on_delete=models.CASCADE,
                               related_name="step_of_recipe")

    def __str__(self):
        return f'StepNumber: {self.step_number}'

