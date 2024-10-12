from django.urls import path
from .views import sport_view

urlpatterns = [
        path('mainsport/', sport_view, name='sport_view'),
    ]