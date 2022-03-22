from django.urls import path, include
from apps.recipe.views.recipe import RecipeCreateView, RecipeRetrieveView, RecipeListView
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('recipe', RecipeView, basename="recipe")

urlpatterns = [
    path('recipe/create/', RecipeCreateView.as_view(), name="recipe-create"),
    path('recipe/<int:pk>/', RecipeRetrieveView.as_view(), name="recipe-retrieve"),
    path('recipe/', RecipeListView.as_view(), name="recipe-list"),
]
# urlpatterns += router.urls