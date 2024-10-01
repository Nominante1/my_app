from django.urls import path
from .views import password_view

urlpatterns = [
    path('password/', password_view, name='password_view'),
]
