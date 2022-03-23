from django.urls import path, include
from apps.recipe.views.recipe import RecipeCreateView, RecipeFavoriteAddView, RecipeRetrieveView, RecipeListView
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('recipe', RecipeView, basename="recipe")

urlpatterns = [
    path('recipe/create/',
         RecipeCreateView.as_view(),
         name="recipe-create"),

    path('recipe/<int:pk>/',
         RecipeRetrieveView.as_view(),
         name="recipe-retrieve"),

    path('recipe/',
         RecipeListView.as_view(),
         name="recipe-list"),

    path('add-recipe/<int:pk>/',
         RecipeFavoriteAddView.as_view(),
         name="favorite-recipe"),
]
# urlpatterns += router.urls