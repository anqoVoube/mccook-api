from django.urls import path, include

urlpatterns = [
    path('', IngredientsView.as_view(), name='ingredients')
]