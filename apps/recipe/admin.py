from django.contrib import admin
from apps.recipe.models.recipe import Recipe
from apps.recipe.models.recipe_steps import RecipeSteps

admin.site.register(Recipe)
admin.site.register(RecipeSteps)