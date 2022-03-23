from django.urls import path, include
from apps.commentrate.views.commentrate import RecipeCommentrateView, DeleteComment, ClientCommentrateView
urlpatterns = [
    path('recipe/<int:pk>/coraun/',
         RecipeCommentrateView.as_view(),
         name="recipe-rate"),

    path('client/<int:pk>/coraun/',
         ClientCommentrateView.as_view(),
         name='client'),

    path('delete-comment/<int:pk>/', DeleteComment.as_view(),
         name="delete-comment")
]