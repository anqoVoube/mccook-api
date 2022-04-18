from django.db import models


class Ingredients(models.Model):
    ingredient_name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.ingredient_name).capitalize()

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'
