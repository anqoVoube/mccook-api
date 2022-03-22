from django.urls import path, include
from apps.client.views.client import UserCreateView, ClientRetrieveView

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='client'),

    path('client/<int:pk>/',
         ClientRetrieveView.as_view(),
         name='client-retrieve')
]