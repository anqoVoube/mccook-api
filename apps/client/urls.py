from django.urls import path, include
from apps.client.views.client import UserCreateView

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='client')
]