from django.urls import path, include
from apps.moderator.views.moderator import RecipeModeratorRetrieveView, RecipeModeratorListView
urlpatterns = [
    path('moderator/<int:pk>/', RecipeModeratorRetrieveView.as_view(), name='moderator-retrieve'),
    path('moderator/', RecipeModeratorListView.as_view(), name='moderator-retrieve'),
]